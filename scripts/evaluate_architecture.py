"""Twenty controlled offline cases. No database, Notion, or Calendar access."""
import json
from pathlib import Path
from time import perf_counter
from simmer.domain import PlanInputs,Interval
from simmer.scheduler import schedule,validate_schedule
from simmer.menu import validate_menu
from simmer.agent import apply_menu_validation

def run():
    root=Path(__file__).resolve().parents[1]
    fixtures=json.loads((root/'docs/reviews/2026-10-29-five-menu-rerun.json').read_text())
    results=[]
    for fixture in fixtures[:5]:
        for condition in ('baseline','more_time','busy_calendar','missing_dependency'):
            data=PlanInputs.model_validate(fixture['inputs'])
            data.availability.status='fixture'
            if condition=='more_time':
                data.gathering.daily_limits={str(d):240 for d in data.gathering.prep_days}
            elif condition=='busy_calendar':
                data.availability.busy=[Interval(start=f'{d}T00:00:00-05:00',end=f'{d}T23:59:00-05:00') for d in data.gathering.prep_days]
            elif condition=='missing_dependency':
                recipe=next(s.recipe for s in data.selections if s.mode=='cook' and s.recipe and s.recipe.tasks)
                recipe.tasks[0].dependencies=['missing-step']
            start=perf_counter()
            plan=apply_menu_validation(data,schedule(data))
            violations=validate_schedule(data,plan)
            menu_issues=[v for v in validate_menu(data) if v.code!='menu_category']
            passed=(plan.status!='feasible' or not violations)
            if condition=='missing_dependency':
                passed=passed and plan.outcome.code=='needs_input'
            if condition=='busy_calendar':
                passed=passed and plan.status!='feasible'
            result={'menu':fixture['name'],'condition':condition,'status':plan.status,'outcome':plan.outcome.model_dump(),'validation_passed':passed,'menu_blockers':[v.code for v in menu_issues],'usable':plan.status=='feasible' and not menu_issues,'violations':[v.model_dump() for v in plan.violations],'seconds':round(perf_counter()-start,2)}
            results.append(result)
            print(f"{fixture['name']} / {condition}: {plan.outcome.code}; checks={passed}",flush=True)
    output=root/'docs/reviews/2026-11-07-architecture-evals.json'
    output.write_text(json.dumps({'scope':'Offline historical fixtures; no live integrations or cooking validation','results':results},indent=2)+'\n')
    return all(r['validation_passed'] for r in results)

if __name__=='__main__':
    raise SystemExit(0 if run() else 1)
