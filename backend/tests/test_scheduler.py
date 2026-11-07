from datetime import datetime, timezone
import pytest
from simmer.domain import *
from simmer.scheduler import schedule, validate_schedule, daily_presence
from simmer.scheduler import tasks_for

def test_combined_prep_feeds_each_cooking_batch():
    i=inputs(); i.gathering.single_batch_kitchen=False; recipe=i.selections[0].recipe
    recipe.servings=5
    recipe.tasks=[PrepTask(id='prep',title='Chop',minutes=15,evidence='estimate',max_ahead_hours=24,scale_mode='combined'), PrepTask(id='cook',title='Cook',minutes=20,evidence='estimate',max_ahead_hours=8,dependencies=['prep'])]
    tasks,issues=tasks_for(i)
    assert not issues
    assert len(tasks)==4
    assert sum('Chop' in t.title for t in tasks)==1
    assert next(t for t in tasks if 'Chop' in t.title).minutes==45
    assert all(t.dependencies==['s:0:prep'] for t in tasks if 'Cook' in t.title)


def inputs(minutes=(40,40),limit=60):
    g=Gathering(arrival='2026-11-06T20:00:00-05:00',earliest_prep='2026-11-06',prep_days=['2026-11-06'],daily_limits={'2026-11-06':limit},prep_windows=[Interval(start='2026-11-06T17:00:00-05:00',end='2026-11-06T19:00:00-05:00')],allergies=[])
    tasks=[PrepTask(id=str(i),title='Cook' if i==0 else 'Cleanup',minutes=m,evidence='Fixture only',max_ahead_hours=48,phase='cooking' if i==0 else 'cleanup') for i,m in enumerate(minutes)]
    r=RecipeSnapshot(id='r',title='Fixture rice',source='fixture',servings=15,reviewed=True,vegetarian=True,allergens=[],tasks=tasks)
    return PlanInputs(gathering=g,selections=[MenuSelection(id='s',title='Rice',recipe=r,servings=15,must_have=True)],availability=AvailabilitySnapshot(status='fixture'))


def test_daily_total_requires_explicit_override():
    i=inputs(); p=schedule(i)
    assert p.status=='conflict'
    assert i.gathering.daily_limits['2026-11-06']==60
    assert p.adjustments and p.adjustments[0].proposed_minutes==90
    i.gathering.daily_limits['2026-11-06']=90
    p=schedule(i)
    assert p.status=='feasible' and not validate_schedule(i,p)
    assert all(a.interval.end<=i.gathering.arrival for a in p.assignments)


def test_unknown_duration_or_storage_not_feasible():
    i=inputs(); i.selections[0].recipe.tasks[0].minutes=None
    assert schedule(i).status=='incomplete'
    i=inputs(); i.selections[0].recipe.tasks[0].max_ahead_hours=None
    assert schedule(i).status=='incomplete'


def test_helper_window_and_capability_are_binding():
    i=inputs(limit=90); i.gathering.profile.helpers=[Helper(id='son',name='Helper',skills=['measure'],available=[Interval(start='2026-11-06T17:00:00-05:00',end='2026-11-06T17:30:00-05:00')])]
    p=schedule(i); p.assignments[0].person='son'
    assert any(v.code=='helper' for v in validate_schedule(i,p))


def test_equipment_dependency_and_deadline_validator():
    i=inputs(limit=120); i.gathering.profile.equipment={'oven':1}
    for t in i.selections[0].recipe.tasks: t.resource='oven'; t.temperature=180
    p=schedule(i)
    p.assignments[1].interval=p.assignments[0].interval.model_copy()
    codes={v.code for v in validate_schedule(i,p)}
    assert 'resource' in codes
    p=schedule(i); p.assignments[0].interval=Interval(start='2026-11-06T19:00:00-05:00',end='2026-11-06T19:40:00-05:00')
    assert any(v.code=='deadline' for v in validate_schedule(i,p))


def test_dst_and_cross_midnight_presence_actual_minutes():
    a=Assignment(task=PrepTask(id='a',title='Supervise',minutes=120),interval=Interval(start='2026-11-01T01:00:00-04:00',end='2026-11-01T02:00:00-05:00'))
    assert daily_presence([a],'America/New_York',[])=={'2026-11-01':120}
    b=Assignment(task=PrepTask(id='b',title='Chill',minutes=120,unattended=True,presence_minutes=0,active_minutes=0),interval=a.interval)
    assert daily_presence([b],'America/New_York',[])=={}
    a.interval=Interval(start='2026-11-05T23:30:00-05:00',end='2026-11-06T00:30:00-05:00')
    assert daily_presence([a],'America/New_York',[])=={'2026-11-05':30,'2026-11-06':30}


def test_protected_time_not_relaxed_by_extra_minutes():
    i=inputs(); i.gathering.profile.protected=i.gathering.prep_windows
    p=schedule(i)
    assert p.status=='conflict' and p.adjustments==[]

def test_validator_cannot_omit_cleanup():
    i=inputs(limit=120); p=schedule(i)
    p.assignments=[a for a in p.assignments if a.task.phase!='cleanup']
    assert any(v.code=='cleanup' for v in validate_schedule(i,p))

def test_each_separate_prep_session_needs_cleanup():
    i=inputs(minutes=(20,),limit=120)
    i.gathering.prep_windows=[Interval(start='2026-11-06T16:00:00-05:00',end='2026-11-06T17:00:00-05:00'),Interval(start='2026-11-06T18:00:00-05:00',end='2026-11-06T19:00:00-05:00')]
    p=schedule(i)
    assert p.status=='feasible'
    p.assignments=[a for a in p.assignments if a.task.phase!='cleanup']
    assert any(v.code=='cleanup' for v in validate_schedule(i,p))

def test_active_work_cannot_disappear_from_presence_budget():
    i=inputs(minutes=(40,),limit=15)
    task=i.selections[0].recipe.tasks[0]
    task.active_minutes=40; task.presence_minutes=0
    i.availability.busy=[Interval(start="2026-11-06T17:00:00-05:00",end="2026-11-06T17:40:00-05:00")]
    assert schedule(i).status!='feasible'

def test_guest_arrival_at_party_time_with_warming_is_conflict_not_crash():
    i=inputs(limit=120)
    i.selections=[MenuSelection(title='Guest dessert',mode='guest',servings=15,contribution=Contribution(name='Dessert',confirmed=True,servings=15,arrival=i.gathering.arrival,warming_minutes=10,equipment='oven'))]
    assert schedule(i).status!='feasible'

def test_unattended_overnight_step_spans_prep_windows_without_consuming_daily_time():
    i=inputs(minutes=(720,),limit=60)
    g=i.gathering; g.arrival=datetime.fromisoformat('2026-11-07T20:00:00-05:00')
    g.prep_days=['2026-11-06','2026-11-07']  # normalize through schema
    i=PlanInputs.model_validate(i.model_dump(mode='json'))
    t=i.selections[0].recipe.tasks[0]; t.unattended=True; t.active_minutes=0; t.presence_minutes=0
    p=schedule(i)
    assert p.status=='feasible'
    assert daily_presence(p.assignments,g.profile.timezone,[])=={}

def test_optional_windows_use_daytime_and_respect_busy_without_mutating_inputs():
    i=inputs(limit=120); i.gathering.prep_windows=[]
    i.availability.busy=[Interval(start='2026-11-06T09:00:00-05:00',end='2026-11-06T17:00:00-05:00')]
    p=schedule(i)
    assert p.status=='feasible'
    assert not validate_schedule(i,p)
    assert i.gathering.prep_windows==[]
    assert all(a.interval.start.hour>=17 for a in p.assignments)

def test_dependency_gap_rejects_overnight_hot_food_pause():
    i=inputs(minutes=(10,15),limit=120)
    r=i.selections[0].recipe
    r.tasks=[PrepTask(id='cook',title='Cook filling',minutes=10,evidence='reviewed',max_ahead_hours=48),PrepTask(id='store',title='Cool and refrigerate',minutes=10,evidence='reviewed',max_ahead_hours=48,dependencies=['cook'],max_dependency_gap_minutes=15)]
    p=schedule(i)
    assert p.status=='feasible'
    store=next(a for a in p.assignments if a.task.id.endswith(':store'))
    from datetime import timedelta
    store.interval=Interval(start=store.interval.start+timedelta(minutes=30),end=store.interval.end+timedelta(minutes=30))
    assert any(v.code=='dependency_gap' for v in validate_schedule(i,p))

def test_constraint_search_preserves_final_dependency_validation():
    from simmer.constraint_scheduler import solve_schedule
    i=inputs(minutes=(15,15),limit=120)
    r=i.selections[0].recipe
    r.tasks=[PrepTask(id='prep',title='Prep',minutes=15,evidence='reviewed',max_ahead_hours=48),PrepTask(id='cook',title='Cook',minutes=15,evidence='reviewed',max_ahead_hours=48,dependencies=['prep'],max_dependency_gap_minutes=15)]
    p=solve_schedule(i)
    assert p.status=='feasible' and not validate_schedule(i,p)
    p.assignments=[a for a in p.assignments if not a.task.id.endswith(':prep')]
    assert any(v.code=='dependency' for v in validate_schedule(i,p))

def test_explicit_serving_task_is_deferred_without_title_guessing():
    from simmer.scheduler import tasks_for, finishing_checklist
    i=inputs(minutes=(10,),limit=120)
    r=i.selections[0].recipe
    r.tasks=[PrepTask(id='cook',title='Cook',minutes=10,evidence='source',max_ahead_hours=24),PrepTask(id='serve',title='Slice roast',minutes=10,evidence='source',phase='serving',dependencies=['cook'])]
    tasks,issues=tasks_for(i)
    assert not issues and len(tasks)==1 and 'Slice roast (at dinner)' in finishing_checklist(i)
    r.tasks[0].title='Carve turkey from vegetables'
    r.tasks[1].phase='cooking';r.tasks[1].max_ahead_hours=24
    assert len(tasks_for(i)[0])==2

def test_serving_task_cannot_hide_prerequisite_work():
    from simmer.scheduler import tasks_for
    i=inputs(minutes=(10,),limit=120)
    i.selections[0].recipe.tasks=[PrepTask(id='serve',title='Serve',minutes=5,evidence='source',phase='serving'),PrepTask(id='prep',title='Cook',minutes=10,evidence='source',max_ahead_hours=24,dependencies=['serve'])]
    assert any(v.code=='dependency' for v in tasks_for(i)[1])
