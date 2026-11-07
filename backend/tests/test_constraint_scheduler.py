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
    assert all(v.code == "allergy_unknown" for v in validate_menu(inputs))
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
