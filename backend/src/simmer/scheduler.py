"""Conservative five-minute heuristic plus independent hard-constraint validator.

No optimality claim. Unknown evidence blocks feasibility. All elapsed arithmetic
uses UTC; local dates only determine daily allowances and selected prep days.
"""
import hashlib, json, math
from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo
from .domain import *
from .availability import overlaps
from .inventory import shopping_for

UTC=timezone.utc

def prep_windows_for(g):
    """Explicit windows win; otherwise search selected local days 09:00–21:00."""
    if g.prep_windows:
        return g.prep_windows
    zone=ZoneInfo(g.profile.timezone)
    windows=[]
    for day in sorted(set(g.prep_days)):
        if g.earliest_prep and day<g.earliest_prep:
            continue
        start=datetime.combine(day,datetime.min.time(),zone).replace(hour=9)
        end=start.replace(hour=21)
        if g.arrival:
            end=min(end,g.arrival-timedelta(minutes=g.relax_minutes))
        if end>start:
            windows.append(Interval(start=start,end=end))
    return windows

def digest(value):
    if hasattr(value,'model_dump'): value=value.model_dump(mode='json')
    return hashlib.sha256(json.dumps(value,sort_keys=True,separators=(',',':')).encode()).hexdigest()

def minutes(a,b): return (b.astimezone(UTC)-a.astimezone(UTC)).total_seconds()/60

def limit_for(g,day):
    return g.daily_limits.get(str(day),g.profile.weekend_minutes if day.weekday()>=5 else g.profile.weekday_minutes)

def occupied(a,helpers,attention=False):
    t=a.task
    helper=next((h for h in helpers if h.id==a.person),None)
    if a.person!='host' and not (helper and helper.supervision): return None
    if helper and helper.supervision: duration=t.minutes or 0
    else:
        duration=t.active_minutes if attention else t.presence_minutes
        if duration is None: duration=0 if t.unattended else t.minutes or 0
    if duration==0: return None
    return Interval(start=a.interval.start,end=min(a.interval.end,a.interval.start.astimezone(UTC)+timedelta(minutes=duration)))

def occupancy_windows(a,helpers,attention=False):
    t=a.task
    helper=next((h for h in helpers if h.id==a.person),None)
    if a.person!='host' and not (helper and helper.supervision): return []
    if t.attention_segments and not (helper and helper.supervision):
        # Presence beyond active work is continuous supervision, not removable waiting.
        active=t.active_minutes or 0
        presence=t.presence_minutes if t.presence_minutes is not None else active
        if attention or presence==active:
            return [Interval(start=a.interval.start.astimezone(UTC)+timedelta(minutes=x.offset_minutes),end=a.interval.start.astimezone(UTC)+timedelta(minutes=x.offset_minutes+x.minutes)) for x in t.attention_segments]
        return [a.interval]
    if attention and not t.attention_segments and t.active_minutes and t.active_minutes<(t.minutes or 0) and t.presence_minutes==t.minutes:
        return [a.interval]  # Unknown attention placement: reserve the whole supervised step.
    window=occupied(a,helpers,attention)
    return [window] if window else []

def daily_presence(assignments,zone,helpers):
    # Union one-minute UTC occupancy, rounded conservatively by scheduled duration.
    slots=set(); tz=ZoneInfo(zone)
    for a in assignments:
        for window in occupancy_windows(a,helpers):
            t=window.start.astimezone(UTC)
            while t<window.end:
                slots.add(t); t+=timedelta(minutes=1)
    result={}
    for t in slots:
        day=t.astimezone(tz).date().isoformat(); result[day]=result.get(day,0)+1
    return result

def tasks_for(inputs):
    tasks=[]; issues=[]
    def issue(code,id,text): issues.append(ConstraintViolation(code=code,affected_ids=[id],explanation=text))
    for s in inputs.selections:
        if s.mode=='buy': continue
        if s.mode=='guest':
            c=s.contribution
            if not c or not c.confirmed or not c.servings or c.warming_minutes is None: issue('contribution',s.id,'Confirm guest servings and warming needs'); continue
            if c.warming_minutes:
                if not c.arrival or not c.equipment or not inputs.gathering.arrival or c.arrival>=inputs.gathering.arrival: issue('contribution',s.id,'Confirm guest arrival and warming equipment'); continue
                tasks.append(PrepTask(id=s.id+':warming',title='Warm '+s.title,minutes=c.warming_minutes,resource=c.equipment,eligible=Interval(start=c.arrival,end=inputs.gathering.arrival),phase='finishing',max_ahead_hours=0,evidence='Host-confirmed guest warming needs'))
            continue
        if s.mode=='semi': original=s.preparation; ratio=1
        else:
            r=s.recipe
            if not r or not r.reviewed or not r.servings: issue('recipe',s.id,'Review recipe, servings and preparation tasks'); continue
            original=r.tasks; ratio=s.servings/r.servings
        if not original: issue('tasks',s.id,'Preparation tasks are missing'); continue
        # Repeat complete cooking batches; partial batch retains full duration conservatively.
        single_batch=inputs.gathering.single_batch_kitchen
        for batch in range(1 if single_batch else math.ceil(ratio)):
            prefix=f'{s.id}:{batch}:'
            for original_task in original:
                if batch and original_task.scale_mode=='combined': continue
                t=original_task.model_copy(deep=True)
                t.id=prefix+t.id; t.recipe_id=s.id
                combined_ids={x.id for x in original if x.scale_mode=='combined'}
                t.dependencies=[f'{s.id}:{0 if d in combined_ids else batch}:'+d for d in t.dependencies]
                t.title=f'{s.title} · {t.title}' + (f' (batch {batch+1})' if ratio>1 and t.scale_mode!='combined' and not single_batch else '')
                fraction=ratio if t.scale_mode=='combined' or single_batch else min(1,ratio-batch)
                t.ingredients=[x.model_copy(update={'quantity':x.quantity*fraction if x.quantity is not None else None}) for x in t.ingredients]
                # Shared preparation happens once, but larger quantities still
                # require more hands-on work. Passive soaking time stays fixed.
                if t.scale_mode=='combined' and ratio>1 and not single_batch and t.minutes is not None:
                    active=t.active_minutes if t.active_minutes is not None else t.minutes
                    added=math.ceil(active*(ratio-1))
                    t.minutes+=added
                    t.active_minutes=active+added
                    t.presence_minutes=(t.presence_minutes if t.presence_minutes is not None else active)+added
                if t.minutes is not None: t.minutes=5*math.ceil(t.minutes/5)
                active=t.active_minutes if t.active_minutes is not None else (0 if t.unattended else t.minutes)
                presence=t.presence_minutes if t.presence_minutes is not None else (0 if t.unattended else t.minutes)
                if active is not None and presence is not None and (active>presence or presence>(t.minutes or 0)): issue('duration',t.id,'Active work must fit within required presence and elapsed time')
                if t.minutes is None or not t.evidence or (t.max_ahead_hours is None and t.preparation_policy!='same_day' and t.phase!='cleanup'): issue('evidence',t.id,'Review task duration and supported preparation/storage window')
                if not t.attention_segments and t.active_minutes and t.active_minutes<(t.minutes or 0):
                    t.presence_minutes=t.minutes
                if t.attention_segments:
                    segments=sorted(t.attention_segments,key=lambda x:x.offset_minutes)
                    if sum(x.minutes for x in segments)!=(t.active_minutes or 0) or any(x.offset_minutes+x.minutes>(t.minutes or 0) for x in segments) or any(a.offset_minutes+a.minutes>b.offset_minutes for a,b in zip(segments,segments[1:])):
                        issue('duration',t.id,'Attention segments must cover active work without overlap and fit elapsed time')
                if t.resource and not inputs.gathering.profile.equipment.get(t.resource): issue('equipment',t.id,'Enter available equipment capacity')
                tasks.append(t)
    return tasks,issues

def content_hash(plan):
    return digest(plan.model_dump(mode='json',exclude={'content_hash','id','generated_at'}))

def validate_schedule(inputs,candidate,partial=False):
    g=inputs.gathering; tz=ZoneInfo(g.profile.timezone); helpers=g.profile.helpers
    expected,issues=tasks_for(inputs); expected={t.id:t for t in expected}
    violations=list(issues)
    def fail(code,text,ids=()): violations.append(ConstraintViolation(code=code,affected_ids=list(ids),explanation=text))
    if not g.arrival or not g.earliest_prep or not g.prep_days or not prep_windows_for(g): fail('setup','Set arrival, prep days and available prep windows'); return violations
    if inputs.availability.status not in ('fresh','fixture'): fail('calendar','Recheck calendar availability')
    if g.allergies is None and not partial: fail('dietary','Confirm allergies, including none')
    by_id={a.task.id:a for a in candidate.assignments}
    if len(by_id)!=len(candidate.assignments): fail('duplicate','Duplicate scheduled task')
    if not partial and any(id not in by_id for id in expected): fail('unscheduled','Some preparation tasks have no feasible slot',[id for id in expected if id not in by_id])
    deadline=g.arrival.astimezone(UTC)-timedelta(minutes=g.relax_minutes)
    finishing=[]
    for a in candidate.assignments:
        t=a.task; window=a.interval
        if t.id not in expected and not t.id.startswith('cleanup:'): fail('unexpected','Unknown task in plan',[t.id]); continue
        if t.id in expected and t!=expected[t.id]: fail('changed_task','Plan task differs from reviewed inputs',[t.id])
        if t.minutes is None: continue
        if minutes(window.start,window.end)!=t.minutes: fail('duration','Task duration changed',[t.id])
        if t.active_minutes is not None and t.active_minutes>t.minutes or t.presence_minutes is not None and t.presence_minutes>t.minutes: fail('duration','Attention/presence exceeds elapsed duration',[t.id])
        if window.start.astimezone(tz).date()<g.earliest_prep: fail('earliest','Task starts before allowed prep date',[t.id])
        if t.phase=='finishing':
            if window.start<deadline or window.end>g.arrival: fail('deadline','Finishing must fit allowed final hour',[t.id])
            finishing.append(a)
        elif window.end>deadline: fail('deadline','Major cooking and cleanup must finish before relaxation time',[t.id])
        if t.eligible and (window.start<t.eligible.start or window.end>t.eligible.end): fail('eligibility','Task falls outside its source-supported window',[t.id])
        if t.preparation_policy=='same_day' and window.start.astimezone(tz).date()!=g.arrival.astimezone(tz).date(): fail('storage','Same-day task cannot be moved to an earlier day',[t.id])
        if t.max_ahead_hours is not None and t.phase=='cooking':
            consumers=[x for x in candidate.assignments if t.id in x.task.dependencies]
            if t.storage_anchor=='next_step':
                if not consumers and not partial: fail('storage','Component storage needs its next preparation step',[t.id])
                targets=[x.interval.start for x in consumers]
            else: targets=[g.arrival]
            if any(minutes(window.end,target)>t.max_ahead_hours*60 for target in targets): fail('storage','Preparation exceeds its supported storage window',[t.id])
        for dep in t.dependencies:
            if dep not in by_id or by_id[dep].interval.end>window.start: fail('dependency','Prerequisite task must finish first',[t.id,dep])
        helper=next((h for h in helpers if h.id==a.person),None)
        if a.person!='host' and (not helper or t.skill not in helper.skills or not any(w.start<=window.start and w.end>=window.end for w in helper.available)): fail('helper','Helper lacks capability or full availability',[t.id])
        for presence in occupancy_windows(a,helpers):
            if not any(w.start<=presence.start and w.end>=presence.end for w in prep_windows_for(g)) and t.phase!='finishing': fail('window','Task needs presence outside chosen prep windows',[t.id])
            if overlaps_any(presence,inputs.availability.busy+g.profile.protected): fail('busy','Task conflicts with calendar or protected time',[t.id])
            for day in daily_presence([a],g.profile.timezone,helpers):
                if datetime.fromisoformat(day).date() not in g.prep_days: fail('day','Task needs presence on an unselected prep day',[t.id])
        if t.resource:
            capacity=g.profile.equipment.get(t.resource)
            simultaneous=[x for x in candidate.assignments if x.task.resource==t.resource and overlaps(x.interval,window)]
            if not capacity or t.capacity>capacity: fail('resource','Equipment capacity unavailable',[t.id])
            # Check each boundary, rather than summing non-overlapping neighbors.
            for point in [x.interval.start for x in simultaneous]+[window.start]:
                active=[x for x in simultaneous if x.interval.start<=point<x.interval.end]
                if capacity and sum(x.task.capacity for x in active)>capacity: fail('resource','Equipment batch capacity exceeded',[t.id])
                temps={x.task.temperature for x in active if x.task.temperature is not None}
                if t.resource=='oven' and len(temps)>1: fail('temperature','Concurrent oven temperatures conflict',[t.id])
    if not partial:
        for session in prep_windows_for(g):
            cooking=[a for a in candidate.assignments if a.task.phase=='cooking' and not (a.task.unattended and a.task.presence_minutes==0) and session.start<=a.interval.start<session.end]
            cleanup=[a for a in candidate.assignments if a.task.phase=='cleanup' and session.start<=a.interval.start and a.interval.end<=session.end]
            if cooking and not any(c.task.minutes and c.task.minutes>=15 and c.interval.start>=max(a.interval.end for a in cooking) for c in cleanup):
                fail('cleanup','Reserve at least 15 minutes of cleanup after each prep session')
    assignments=candidate.assignments
    for index,a in enumerate(assignments):
        for b in assignments[index+1:]:
            if a.person==b.person and a.person!='host' and overlaps(a.interval,b.interval): fail('attention','Helper double-booked',[a.task.id,b.task.id])
            if any(overlaps(aa,bb) for aa in occupancy_windows(a,helpers,True) for bb in occupancy_windows(b,helpers,True)): fail('attention','Host attention double-booked',[a.task.id,b.task.id])
    cooking_totals=daily_presence([a for a in assignments if a.task.phase!='cleanup'],g.profile.timezone,helpers)
    for day,total in daily_presence(assignments,g.profile.timezone,helpers).items():
        allowance=min(g.cleanup_overrun_minutes,total-cooking_totals.get(day,0))
        if total-allowance>limit_for(g,datetime.fromisoformat(day).date()): fail('daily_limit',f'{day}: {total} minutes exceeds daily total including cleanup allowance',[day])
    if sum(daily_presence(finishing,g.profile.timezone,helpers).values())>g.finishing_minutes: fail('finishing','Final-hour finishing allowance exceeded')
    return violations

def overlaps_any(window,others): return any(overlaps(window,x) for x in others)

def _schedule(inputs,priority=False):
    g=inputs.gathering
    p=PlanCandidate(gathering_id=g.id,revision=g.revision,input_hash=digest(inputs),shopping=shopping_for(inputs),checklist=['Keep dishes warm as directed','Transfer to serving dishes','Check serving spoons','Finish drinks'])
    tasks,issues=tasks_for(inputs)
    if issues or not g.arrival or not prep_windows_for(g):
        p.violations=issues or [ConstraintViolation(code='setup',explanation='Complete gathering times and prep windows')]; return p
    remaining=list(tasks); scheduled=set(); attempts=0
    while remaining and attempts<20000:
        ready=[t for t in remaining if all(d in scheduled for d in t.dependencies)]
        if priority: ready.sort(key=lambda t:t.eligible.end if t.eligible else g.arrival)
        if not ready: break
        placed=False
        for task in ready:
            windows=prep_windows_for(g) if task.phase!='finishing' else [Interval(start=g.arrival-timedelta(minutes=g.relax_minutes),end=g.arrival)]
            for window in windows:
                start=window.start.astimezone(UTC)
                start+=timedelta(minutes=(-start.minute)%5,seconds=-start.second,microseconds=-start.microsecond)
                elapsed_end=g.arrival-timedelta(minutes=g.relax_minutes) if task.unattended and task.presence_minutes==0 else window.end
                while start<window.end and start+timedelta(minutes=task.minutes or 0)<=elapsed_end and attempts<20000:
                    end=start+timedelta(minutes=task.minutes or 0); attempts+=1
                    for person in ['host']+[h.id for h in g.profile.helpers if task.skill in h.skills]:
                        assignment=Assignment(task=task,interval=Interval(start=start,end=end),person=person)
                        trial=p.model_copy(update={'assignments':p.assignments+[assignment]})
                        # Reserve cleanup while placing work, so it cannot push a
                        # fully used daily allowance over the limit afterward.
                        projected=list(trial.assignments)
                        for index,session in enumerate(prep_windows_for(g)):
                            cooking=[a for a in trial.assignments if a.task.phase=='cooking' and not (a.task.unattended and a.task.presence_minutes==0) and session.start<=a.interval.start<session.end]
                            cleanup=[a for a in trial.assignments if a.task.phase=='cleanup' and session.start<=a.interval.start and a.interval.end<=session.end]
                            if cooking and not cleanup:
                                cleanup_start=max(a.interval.end for a in cooking)
                                projected.append(Assignment(task=PrepTask(id='cleanup:'+str(index),title='Cleanup',minutes=15,phase='cleanup',evidence='Planning allowance'),interval=Interval(start=cleanup_start,end=cleanup_start+timedelta(minutes=15))))
                        trial=trial.model_copy(update={'assignments':projected})
                        if not validate_schedule(inputs,trial,partial=True):
                            p.assignments.append(assignment); scheduled.add(task.id); remaining.remove(task); placed=True; break
                    if placed: break
                    start+=timedelta(minutes=5)
                if placed: break
            if placed: break
        if not placed: break
    # Each chosen prep session needs cleanup, including when helpers do the cooking.
    for index,session in enumerate(prep_windows_for(g)):
        cooking=[a for a in p.assignments if a.task.phase=='cooking' and not (a.task.unattended and a.task.presence_minutes==0) and session.start<=a.interval.start<session.end]
        cleanup=[a for a in p.assignments if a.task.phase=='cleanup' and session.start<=a.interval.start and a.interval.end<=session.end]
        if not cooking or cleanup: continue
        start=max(a.interval.end for a in cooking)
        task=PrepTask(id='cleanup:'+str(index),title='Cleanup',minutes=15,phase='cleanup',evidence='Planning allowance: 15-minute cleanup estimate')
        p.assignments.append(Assignment(task=task,interval=Interval(start=start,end=start+timedelta(minutes=15))))
    p.violations=validate_schedule(inputs,p)
    p.status='conflict' if p.violations else 'feasible'
    return p

def schedule(inputs):
    plan=_schedule(inputs)
    if plan.status=='conflict':
        alternative=_schedule(inputs,priority=True)
        if alternative.status=='feasible' or len(alternative.assignments)>len(plan.assignments): plan=alternative
    if plan.status=='conflict':
        # Validate each concrete +30-minute proposal; never silently apply it.
        for day in inputs.gathering.prep_days[:14]:
            trial=inputs.model_copy(deep=True); current=limit_for(trial.gathering,day)
            trial.gathering.daily_limits[str(day)]=min(1440,current+30)
            candidate=_schedule(trial)
            if candidate.status=='feasible':
                window=next((w for w in prep_windows_for(trial.gathering) if w.start.astimezone(ZoneInfo(trial.gathering.profile.timezone)).date()==day),None)
                plan.adjustments.append(TimeAdjustment(day=day,current_minutes=current,proposed_minutes=current+30,window=window,reason='This candidate fits with 30 additional minutes within your existing free window; it is not a minimum-time guarantee.'))
    plan.fit_days=fit_summary(inputs,plan)
    plan.content_hash=content_hash(plan)
    return plan

def suggest_time_adjustments(inputs,violations): return schedule(inputs).adjustments

def fit_summary(inputs,plan):
    g=inputs.gathering
    total=daily_presence(plan.assignments,g.profile.timezone,g.profile.helpers)
    cooking=daily_presence([a for a in plan.assignments if a.task.phase!='cleanup'],g.profile.timezone,g.profile.helpers)
    return [{'day':str(day),'presence_minutes':total.get(str(day),0),'cooking_minutes':cooking.get(str(day),0),'limit_minutes':limit_for(g,day),'cleanup_allowance':g.cleanup_overrun_minutes} for day in sorted(g.prep_days)]
