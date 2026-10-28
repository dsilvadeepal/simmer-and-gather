from datetime import datetime, timezone
import pytest
from simmer.domain import *
from simmer.scheduler import schedule, validate_schedule, daily_presence


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
