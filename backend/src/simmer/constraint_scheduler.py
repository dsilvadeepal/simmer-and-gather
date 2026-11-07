"""Bounded deterministic fallback for a solo host; independent validation is mandatory.

Models whole recipe chains together instead of committing to greedy early slots.
Unsupported helper/finishing configurations fall back to the existing scheduler.
"""
from datetime import datetime,timedelta,timezone
from zoneinfo import ZoneInfo
from collections import defaultdict
from ortools.sat.python import cp_model
from .domain import Assignment,Interval,PrepTask,PlanCandidate

def solve_schedule(inputs,time_limit=5,diagnostics=None):
    from .scheduler import tasks_for,prep_windows_for,limit_for,digest,validate_schedule,content_hash,fit_summary,finishing_checklist
    from .inventory import shopping_for
    if diagnostics is not None: diagnostics['solver_status']='UNSUPPORTED'
    g=inputs.gathering
    tasks,issues=tasks_for(inputs);windows=prep_windows_for(g)
    if issues or not tasks or not g.arrival or not g.earliest_prep or not windows or g.profile.helpers or any(t.phase!='cooking' for t in tasks):return None
    zone=ZoneInfo(g.profile.timezone)
    if len({w.start.astimezone(zone).date() for w in windows})!=len(windows):return None
    origin=datetime.combine(g.earliest_prep,datetime.min.time(),zone).astimezone(timezone.utc)
    def tick(dt):return int((dt.astimezone(timezone.utc)-origin).total_seconds()//60)
    deadline=tick(g.arrival)-g.relax_minutes;arrival=tick(g.arrival)
    if deadline<=0 or deadline>20160:return None
    model=cp_model.CpModel();starts={};ends={};all_intervals={};human=[];resources=defaultdict(list);chosen={};weights={};objective=[]
    for t in tasks:
        starts[t.id]=model.new_int_var(0,deadline,'start:'+t.id)
        ends[t.id]=model.new_int_var(0,deadline,'end:'+t.id)
        # Five-minute search grid, retaining exact reviewed elapsed duration.
        grid=model.new_int_var(0,deadline//5,'grid:'+t.id);model.add(starts[t.id]==grid*5)
        all_intervals[t.id]=model.new_interval_var(starts[t.id],t.minutes,ends[t.id],t.id)
        if t.eligible:model.add(starts[t.id]>=tick(t.eligible.start));model.add(ends[t.id]<=tick(t.eligible.end))
        if t.max_ahead_hours is not None and t.storage_anchor=='serving':model.add(ends[t.id]>=arrival-int(t.max_ahead_hours*60))
        if t.resource:resources[t.resource].append((all_intervals[t.id],t.capacity,t.temperature))
        presence=t.presence_minutes if t.presence_minutes is not None else t.minutes
        weights[t.id]=presence
        if presence:
            # Full-presence steps reserve continuous attention conservatively.
            segments=[(s.offset_minutes,s.minutes) for s in t.attention_segments] if t.attention_segments and presence==(t.active_minutes or 0) else [(0,presence)]
            for k,(offset,length) in enumerate(segments):human.append(model.new_interval_var(starts[t.id]+offset,length,starts[t.id]+offset+length,f'attention:{t.id}:{k}'))
            flags=[]
            for j,w in enumerate(windows):
                flag=model.new_bool_var(f'day:{t.id}:{j}');chosen[t.id,j]=flag;flags.append(flag)
                model.add(starts[t.id]>=tick(w.start)).only_enforce_if(flag)
                model.add(ends[t.id]<=tick(w.end)).only_enforce_if(flag)
                if t.preparation_policy=='same_day' and w.start.astimezone(zone).date()!=g.arrival.astimezone(zone).date():model.add(flag==0)
            model.add_exactly_one(flags)
        elif t.preparation_policy=='same_day':
            model.add(starts[t.id]>=tick(datetime.combine(g.arrival.astimezone(zone).date(),datetime.min.time(),zone)))
        # Prefer earlier safe make-ahead work and later fresh finishing.
        objective.append(starts[t.id] if (t.max_ahead_hours or 0)>=12 and t.storage_anchor=='serving' else -starts[t.id])
    for t in tasks:
        for d in t.dependencies:
            if d not in ends:return None
            model.add(starts[t.id]>=ends[d]+t.min_dependency_gap_minutes)
        if t.dependencies and t.max_dependency_gap_minutes is not None:
            last=model.new_int_var(0,deadline,'last:'+t.id);model.add_max_equality(last,[ends[d] for d in t.dependencies]);model.add(starts[t.id]<=last+t.max_dependency_gap_minutes)
        if t.storage_anchor=='next_step' and t.max_ahead_hours is not None:
            children=[c for c in tasks if t.id in c.dependencies]
            if not children:return None
            for child in children:model.add(starts[child.id]-ends[t.id]<=int(t.max_ahead_hours*60))
    cleanups=[]
    for j,w in enumerate(windows):
        pairs=[(t,chosen[t.id,j]) for t in tasks if (t.id,j) in chosen]
        used=model.new_bool_var('used:'+str(j));model.add_max_equality(used,[flag for _,flag in pairs])
        end_vars=[];start_vars=[]
        for t,flag in pairs:
            end=model.new_int_var(0,deadline,'dayend:'+t.id+':'+str(j));model.add(end==ends[t.id]).only_enforce_if(flag);model.add(end==0).only_enforce_if(flag.Not());end_vars.append(end)
            begin=model.new_int_var(0,deadline,'daystart:'+t.id+':'+str(j));model.add(begin==starts[t.id]).only_enforce_if(flag);model.add(begin==deadline).only_enforce_if(flag.Not());start_vars.append(begin)
        first=model.new_int_var(0,deadline,'first:'+str(j));model.add_min_equality(first,start_vars)
        end=model.new_int_var(0,deadline,'cleanup-start:'+str(j));model.add_max_equality(end,end_vars)
        span=model.new_int_var(0,deadline,'span:'+str(j));model.add(span==end-first).only_enforce_if(used);model.add(span==0).only_enforce_if(used.Not());objective.append(5*span)
        cleanup_start=model.new_int_var(0,deadline,'cleanup-flex:'+str(j))
        # Clean during a passive cooking gap, not necessarily after the last dish.
        # Retain the full allowance and host-attention/calendar constraints.
        model.add(cleanup_start>=first+5).only_enforce_if(used)
        model.add(cleanup_start+15<=tick(w.end)).only_enforce_if(used)
        model.add(cleanup_start+15<=deadline).only_enforce_if(used)
        cleanup=model.new_optional_interval_var(cleanup_start,15,cleanup_start+15,used,'cleanup:'+str(j));human.append(cleanup)
        allowance=min(15,g.cleanup_overrun_minutes)
        model.add(sum(weights[t.id]*flag for t,flag in pairs)+(15-allowance)*used<=limit_for(g,w.start.astimezone(zone).date()))
        cleanups.append((j,cleanup_start,used))
    # Busy windows may overlap each other: merge before adding fixed exclusions.
    busy=sorted((max(0,tick(w.start)),min(deadline,tick(w.end))) for w in inputs.availability.busy+g.profile.protected if tick(w.end)>0 and tick(w.start)<deadline)
    merged=[]
    for a,b in busy:
        if merged and a<=merged[-1][1]:merged[-1]=(merged[-1][0],max(b,merged[-1][1]))
        else:merged.append((a,b))
    for j,(a,b) in enumerate(merged):human.append(model.new_fixed_size_interval_var(a,b-a,'busy:'+str(j)))
    model.add_no_overlap(human)
    for resource,rows in resources.items():
        capacity=g.profile.equipment.get(resource)
        if not capacity:return None
        model.add_cumulative([r[0] for r in rows],[r[1] for r in rows],capacity)
        if resource=='oven':
            for k,a in enumerate(rows):
                for b in rows[k+1:]:
                    if a[2] is not None and b[2] is not None and a[2]!=b[2]:model.add_no_overlap([a[0],b[0]])
    model.minimize(sum(objective))
    solver=cp_model.CpSolver();solver.parameters.max_time_in_seconds=time_limit;solver.parameters.num_search_workers=1;solver.parameters.random_seed=44
    status=solver.solve(model)
    if diagnostics is not None: diagnostics['solver_status']=solver.status_name(status)
    if status not in (cp_model.FEASIBLE,cp_model.OPTIMAL):return None
    assignments=[Assignment(task=t,interval=Interval(start=origin+timedelta(minutes=solver.value(starts[t.id])),end=origin+timedelta(minutes=solver.value(ends[t.id])))) for t in tasks]
    for j,end,used in cleanups:
        if solver.value(used):
            start=origin+timedelta(minutes=solver.value(end))
            assignments.append(Assignment(task=PrepTask(id='cleanup:'+str(j),title='Cleanup',minutes=15,phase='cleanup',evidence='Planning allowance'),interval=Interval(start=start,end=start+timedelta(minutes=15))))
    p=PlanCandidate(gathering_id=g.id,revision=g.revision,input_hash=digest(inputs),assignments=sorted(assignments,key=lambda a:a.interval.start),shopping=shopping_for(inputs),checklist=finishing_checklist(inputs))
    p.violations=validate_schedule(inputs,p)
    if diagnostics is not None: diagnostics['validation']=[v.model_dump() for v in p.violations]
    if p.violations:return None
    p.status='feasible';p.fit_days=fit_summary(inputs,p);p.content_hash=content_hash(p)
    return p
