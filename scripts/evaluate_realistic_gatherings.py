"""Repeatable current-library scenarios; no integrations or application writes."""
import json,sys
from pathlib import Path
from time import perf_counter
from simmer.domain import PlanInputs
from simmer.scheduler import schedule,validate_schedule
from simmer.agent import apply_menu_validation
ROOT=Path(__file__).resolve().parents[1]

def evaluate(data):
    before=data.model_dump(mode='json')
    start=perf_counter()
    plan=apply_menu_validation(data,schedule(data))
    checks=validate_schedule(data,plan)
    assert data.model_dump(mode='json')==before
    return {'status':plan.status,'outcome':plan.outcome.model_dump(),'violations':[v.model_dump() for v in plan.violations], 'validator_codes':[v.code for v in checks], 'assignment_count':len(plan.assignments),'fit_days':plan.fit_days,'seconds':round(perf_counter()-start,2),'plan':plan.model_dump(mode='json')}

def run(label='before'):
    rows=[]
    output=ROOT/f'docs/reviews/2026-11-07-realistic-{label}.json'
    for case in json.loads((ROOT/('evals/realistic-free-calendar.json' if label=='before' else 'evals/realistic-free-calendar-corrected.json')).read_text()):
        result=evaluate(PlanInputs.model_validate(case['inputs']))
        row={'id':case['id'],'name':case['name'],**result};rows.append(row)
        output.write_text(json.dumps(rows,indent=2)+'\n')
        print(case['name'],result['outcome']['code'], sorted({v['code'] for v in result['violations']}),flush=True)
    return rows
if __name__=='__main__':run(sys.argv[1] if len(sys.argv)>1 else 'before')
