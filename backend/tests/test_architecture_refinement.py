from datetime import timedelta
from simmer.domain import *
from simmer.scheduler import schedule, validate_schedule, daily_presence
from test_scheduler import inputs

def test_explicit_same_day_does_not_require_invented_storage():
    i=inputs(minutes=(20,),limit=60)
    t=i.selections[0].recipe.tasks[0]
    t.max_ahead_hours=None
    t.preparation_policy='same_day'
    p=schedule(i)
    assert p.status=='feasible'
    assert p.assignments[0].interval.start.date()==i.gathering.arrival.date()

def test_end_attention_counts_and_cannot_overlap_calendar():
    i=inputs(minutes=(60,),limit=60)
    t=i.selections[0].recipe.tasks[0]
    t.active_minutes=10; t.presence_minutes=10
    t.attention_segments=[AttentionSegment(offset_minutes=0,minutes=5),AttentionSegment(offset_minutes=55,minutes=5)]
    p=schedule(i)
    a=p.assignments[0]
    assert daily_presence([a],i.gathering.profile.timezone,[])=={'2026-11-06':10}
    i.availability.busy=[Interval(start=a.interval.end-timedelta(minutes=5),end=a.interval.end)]
    assert 'busy' in {v.code for v in validate_schedule(i,p)}

def test_storage_can_be_anchored_to_next_step():
    i=inputs(minutes=(20,),limit=120)
    t=i.selections[0].recipe.tasks[0]
    t.max_ahead_hours=1; t.storage_anchor='next_step'
    i.selections[0].recipe.tasks.append(PrepTask(id='finish',title='Finish',minutes=10,dependencies=[t.id],max_ahead_hours=8,evidence='fixture'))
    p=schedule(i)
    assert p.status=='feasible'

def test_single_batch_default_preserves_scaled_ingredients():
    i=inputs(minutes=(20,),limit=60)
    i.selections[0].recipe.servings=5
    i.selections[0].recipe.tasks[0].ingredients=[Ingredient(name='rice',quantity=1,unit='cup')]
    from simmer.scheduler import tasks_for
    ts,issues=tasks_for(i)
    assert len(ts)==1 and ts[0].ingredients[0].quantity==3

def test_optional_menu_counts_do_not_block_schedule(store,owner):
    from simmer.profiles import HostingService
    from simmer.agent import PlanningService
    i=inputs(minutes=(20,),limit=60)
    g=HostingService(store).save_gathering(owner,i.gathering,None)
    service=PlanningService(store)
    edited=service.apply_menu_changes(owner,g.id,[{'action':'add','selection':i.selections[0].model_dump(mode='json')}],g.revision)
    p=service.generate_final_plan(owner,g.id,edited.gathering.revision,i.availability)
    assert p.status=='feasible'
    assert p.advisories and not p.violations

def test_failed_current_plan_never_substitutes_old_assignments(store):
    from fastapi.testclient import TestClient
    from simmer.api import create_app
    from test_api import Auth
    from simmer.profiles import HostingService
    owner='api-test-owner'; i=inputs(minutes=(20,),limit=60)
    g=HostingService(store).save_gathering(owner,i.gathering,None)
    old=schedule(i); old.gathering_id=g.id; old.revision=g.revision
    store.put(owner,'plan',old.id,{'plan':old.model_dump(mode='json'),'inputs':i.model_dump(mode='json')})
    new=PlanCandidate(gathering_id=g.id,revision=g.revision,input_hash='new')
    store.put(owner,'plan',new.id,{'plan':new.model_dump(mode='json'),'inputs':i.model_dump(mode='json')})
    ws=TestClient(create_app(store,Auth(),fixture_mode=True)).get('/api/workspace/'+g.id,headers={'Authorization':'Bearer test'}).json()
    assert ws['plan']['id']==new.id
    assert ws['plan']['assignments']==[]
    assert ws['previous_plan']['id']==old.id

def test_attention_end_is_in_calendar_proposal():
    from simmer.approval import event_proposals
    i=inputs(minutes=(60,),limit=60)
    t=i.selections[0].recipe.tasks[0]; t.active_minutes=10; t.presence_minutes=10
    t.attention_segments=[AttentionSegment(offset_minutes=0,minutes=5),AttentionSegment(offset_minutes=55,minutes=5)]
    p=schedule(i)
    events=event_proposals('owner',p,i)
    assert any(datetime.fromisoformat(e['start']['dateTime'])==p.assignments[0].interval.end-timedelta(minutes=5) for e in events)

def test_fit_summary_uses_presence_not_sum_of_elapsed():
    from simmer.scheduler import fit_summary
    i=inputs(minutes=(60,),limit=60)
    t=i.selections[0].recipe.tasks[0];t.active_minutes=10;t.presence_minutes=10
    t.attention_segments=[AttentionSegment(offset_minutes=0,minutes=5),AttentionSegment(offset_minutes=55,minutes=5)]
    p=schedule(i)
    summary=fit_summary(i,p)
    assert summary[0]['presence_minutes']==25
    assert summary[0]['cooking_minutes']==10
    assert summary[0]['limit_minutes']==60

def test_planning_links_safe_schedule_and_validation_traces(store,owner):
    from simmer.telemetry import Telemetry
    from simmer.agent import PlanningService
    from simmer.profiles import HostingService
    calls=[]
    class Client:
        def create_run(self,**kwargs): calls.append(kwargs)
    i=inputs(minutes=(20,),limit=60)
    g=HostingService(store).save_gathering(owner,i.gathering,None)
    service=PlanningService(store,telemetry=Telemetry(Client()))
    changed=service.apply_menu_changes(owner,g.id,[{'action':'add','selection':i.selections[0].model_dump(mode='json')}],1)
    service.generate_final_plan(owner,g.id,changed.gathering.revision,i.availability)
    parent=next(c for c in calls if c['name']=='hosting-plan')
    children=[c for c in calls if c.get('parent_run_id')==parent['id']]
    assert {c['name'] for c in children}=={'build_prep_schedule','validate_hosting_plan'}
    assert all(c['inputs']=={} for c in calls)

def test_changed_recipe_blocks_approval_even_when_gathering_revision_unchanged(store,owner):
    from simmer.approval import ApprovalService
    from simmer.db import Conflict
    from simmer.profiles import HostingService
    from simmer.agent import PlanningService
    from simmer.recipes import RecipeService
    import pytest
    i=inputs(minutes=(20,),limit=60);i.availability.status='fresh'
    g=HostingService(store).save_gathering(owner,i.gathering,None)
    service=PlanningService(store)
    changed=service.apply_menu_changes(owner,g.id,[{'action':'add','selection':i.selections[0].model_dump(mode='json')}],1)
    p=service.generate_final_plan(owner,g.id,changed.gathering.revision,i.availability)
    r=i.selections[0].recipe.model_copy(deep=True);r.version='changed'
    store.put(owner,'recipe',r.id,r.model_dump(mode='json'))
    with pytest.raises(Conflict,match='Recipe collection changed'):
        ApprovalService(store).approve_plan(owner,p.id,p.revision,p.content_hash)

def test_readiness_distinguishes_same_day_from_advance():
    from simmer.recipe_readiness import readiness
    i=inputs(minutes=(20,));r=i.selections[0].recipe
    r.ingredients=[Ingredient(name='rice',quantity=1,unit='cup')]
    r.tasks[0].max_ahead_hours=None;r.tasks[0].preparation_policy='same_day'
    flags=readiness(r)
    assert flags['ingredients'] and flags['steps'] and flags['timing']
    assert flags['same_day'] and not flags['advance_preparation']

def test_bounded_rearrangement_tries_tight_task_first():
    i=inputs(minutes=(30,),limit=90)
    r=i.selections[0].recipe.model_copy(deep=True);r.id='tight'
    r.tasks[0].eligible=Interval(start='2026-11-06T17:00:00-05:00',end='2026-11-06T17:30:00-05:00')
    i.selections.append(MenuSelection(id='tight',title='Time sensitive',recipe=r,servings=15))
    p=schedule(i)
    assert p.status=='feasible' and not p.adjustments
    assert i.gathering.daily_limits['2026-11-06']==90

def test_legacy_mixed_step_is_conservative_until_attention_is_refined():
    from simmer.scheduler import tasks_for
    i=inputs(minutes=(60,),limit=120)
    t=i.selections[0].recipe.tasks[0];t.active_minutes=10;t.presence_minutes=10
    tasks,_=tasks_for(i)
    assert tasks[0].presence_minutes==60

def test_workspace_recheck_marks_new_calendar_conflict(store,owner):
    from fastapi.testclient import TestClient
    from simmer.api import create_app
    from simmer.profiles import HostingService
    from simmer.agent import PlanningService
    i=inputs(minutes=(20,),limit=60)
    g=HostingService(store).save_gathering(owner,i.gathering,None)
    svc=PlanningService(store)
    updated=svc.apply_menu_changes(owner,g.id,[{'action':'add','selection':i.selections[0].model_dump(mode='json')}],1)
    p=svc.generate_final_plan(owner,g.id,updated.gathering.revision,i.availability)
    class Auth:
        def require_owner(self,token):return owner
    class Calendar:
        def read_availability(self,*args,**kwargs):return AvailabilitySnapshot(status='fresh',busy=[p.assignments[0].interval])
    ws=TestClient(create_app(store,Auth(),availability=Calendar())).get('/api/workspace/'+g.id,headers={'Authorization':'Bearer test'}).json()
    assert ws['plan']['status']=='conflict'
    assert any(v['code']=='busy' for v in ws['plan']['violations'])
    assert store.get(owner,'plan',p.id)[0]['plan']['status']=='feasible'
