import json
from pathlib import Path
import pytest
from simmer.domain import PlanInputs,Interval
from simmer.constraint_scheduler import solve_schedule
from simmer.scheduler import validate_schedule
from simmer.menu import validate_menu

CASES=json.loads((Path(__file__).parent/'fixtures/five_hosting_menus.json').read_text())

@pytest.mark.parametrize('row',CASES,ids=[r['name'] for r in CASES])
def test_five_menus_fit_without_expanding_limits(row):
    inputs=PlanInputs.model_validate(row['inputs']);before=inputs.model_dump(mode='json')
    result=solve_schedule(inputs,time_limit=5)
    assert result is not None and result.status=='feasible'
    assert not validate_schedule(inputs,result)
    # Dietary screening must not certify that products are allergen-free.
    assert all(v.code in ("allergy_unknown", "allergy_label_check") for v in validate_menu(inputs))
    assert inputs.model_dump(mode='json')==before
    assert all(a.interval.end<=inputs.gathering.arrival.replace(hour=17,minute=30) for a in result.assignments)

def test_busy_whole_prep_period_is_not_ignored():
    inputs=PlanInputs.model_validate(CASES[0]['inputs'])
    inputs.availability.busy=[Interval(start='2026-12-22T00:00:00-05:00',end='2026-12-26T00:00:00-05:00')]
    assert solve_schedule(inputs) is None

def test_impossible_time_limits_are_not_relaxed():
    inputs=PlanInputs.model_validate(CASES[0]['inputs'])
    inputs.gathering.daily_limits={str(d):0 for d in inputs.gathering.prep_days}
    assert solve_schedule(inputs) is None

def test_turkey_carving_is_dinner_checklist_not_prep_work():
    from simmer.scheduler import tasks_for, finishing_checklist
    row=next(r for r in CASES if r['name']=='Thanksgiving')
    inputs=PlanInputs.model_validate(row['inputs'])
    tasks,issues=tasks_for(inputs)
    assert not any('carve turkey' in t.title.lower() for t in tasks)
    assert 'Carve turkey into serving portions (at dinner)' in finishing_checklist(inputs)
    assert not any(v.code=='dependency' for v in issues)
    turkey=next(s for s in inputs.selections if 'Turkey' in s.title)
    turkey.mode='buy'
    assert 'Carve turkey into serving portions (at dinner)' not in finishing_checklist(inputs)

def test_cleanup_can_use_passive_cooking_time_without_eroding_buffer():
    from test_scheduler import inputs as make_inputs
    from simmer.domain import PrepTask, AttentionSegment
    data=make_inputs(minutes=(30,),limit=90)
    data.selections[0].recipe.tasks=[PrepTask(id='fresh',title='Cook fresh dish',minutes=30,active_minutes=10,presence_minutes=10,attention_segments=[AttentionSegment(offset_minutes=0,minutes=5),AttentionSegment(offset_minutes=25,minutes=5)],max_ahead_hours=data.gathering.relax_minutes/60,evidence='Fixture: finish exactly at buffer',preparation_policy='same_day')]
    p=solve_schedule(data)
    assert p is not None
    assert not validate_schedule(data,p)
    cooking=next(a for a in p.assignments if a.task.id.endswith(':fresh'))
    cleanup=next(a for a in p.assignments if a.task.phase=='cleanup')
    assert cooking.interval.start<cleanup.interval.start<cleanup.interval.end<cooking.interval.end
    assert (data.gathering.arrival-cooking.interval.end).total_seconds()==data.gathering.relax_minutes*60

def test_optional_short_helper_does_not_disable_host_only_fallback():
    from simmer.domain import Helper
    inputs=PlanInputs.model_validate(CASES[0]['inputs'])
    from datetime import timedelta
    start=inputs.gathering.arrival-timedelta(days=1)
    inputs.gathering.profile.helpers=[Helper(id='short',name='Optional helper',skills=['cook'],available=[Interval(start=start,end=start+timedelta(minutes=30))])]
    before=inputs.model_dump(mode='json')
    result=solve_schedule(inputs)
    assert result is not None
    assert all(a.person=='host' for a in result.assignments)
    assert not validate_schedule(inputs,result)
    assert inputs.model_dump(mode='json')==before
