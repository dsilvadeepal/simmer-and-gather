"""Upload synthetic case labels and redacted scheduler results to LangSmith."""
import json
from pathlib import Path
from langsmith import Client
from simmer.domain import PlanInputs, Interval
from simmer.scheduler import schedule, validate_schedule
from simmer.agent import apply_menu_validation

ROOT = Path(__file__).resolve().parents[1]

def main():
    values = dict(line.split('=', 1) for line in (ROOT / '.env.langsmith-evals').read_text().splitlines() if '=' in line)
    client = Client(api_key=values['LANGSMITH_EVAL_API_KEY'])
    fixtures = json.loads((ROOT / 'docs/reviews/2026-10-29-five-menu-rerun.json').read_text())[:5]
    name = 'simmer-hosting-regression-v1'
    if client.has_dataset(dataset_name=name):
        dataset = client.read_dataset(dataset_name=name)
    else:
        dataset = client.create_dataset(name, description='20 offline scheduler regression cases. Synthetic availability; no live calendar access. Only case labels and redacted outcomes are uploaded.')
        for i in range(len(fixtures)):
            for condition in ('baseline', 'more_time', 'busy_calendar', 'missing_dependency'):
                client.create_example(inputs={'menu_index': i, 'condition': condition}, outputs={'valid_complete_only': True}, dataset_id=dataset.id)

    def target(inputs):
        data = PlanInputs.model_validate(fixtures[inputs['menu_index']]['inputs'])
        data.availability.status = 'fixture'
        condition = inputs['condition']
        if condition == 'more_time':
            data.gathering.daily_limits = {str(d): 240 for d in data.gathering.prep_days}
        elif condition == 'busy_calendar':
            data.availability.busy = [Interval(start=f'{d}T00:00:00-05:00', end=f'{d}T23:59:00-05:00') for d in data.gathering.prep_days]
        elif condition == 'missing_dependency':
            recipe = next(s.recipe for s in data.selections if s.mode == 'cook' and s.recipe and s.recipe.tasks)
            recipe.tasks[0].dependencies = ['missing-step']
        plan = apply_menu_validation(data, schedule(data))
        violations = validate_schedule(data, plan)
        return {'menu': fixtures[inputs['menu_index']]['name'], 'condition': condition, 'status': plan.status, 'outcome': plan.outcome.code, 'validator_codes': [v.code for v in violations], 'task_count': len(plan.assignments)}

    def validity(inputs, outputs):
        return {'key': 'valid_complete_only', 'score': int(outputs['status'] != 'feasible' or not outputs['validator_codes'])}

    def constraints(inputs, outputs):
        condition = inputs['condition']
        ok = (condition != 'busy_calendar' or outputs['status'] != 'feasible') and (condition != 'missing_dependency' or outputs['outcome'] == 'needs_input')
        return {'key': 'constraint_handling', 'score': int(ok)}

    def expected_outcome(inputs, outputs):
        expected = {'baseline': 'complete', 'more_time': 'complete', 'busy_calendar': 'no_fit_found', 'missing_dependency': 'needs_input'}[inputs['condition']]
        return {'key': 'expected_outcome', 'score': int(outputs['outcome'] == expected), 'comment': f'Expected {expected}; got {outputs["outcome"]}'}

    def completion(inputs, outputs):
        return {'key': 'complete_plan', 'score': int(outputs['outcome'] == 'complete')}

    result = client.evaluate(target, data=dataset.name, evaluators=[validity, constraints, expected_outcome, completion], experiment_prefix='hosting-regression-reviewed', description='Actual local scheduler rerun; correctness and completion are separate scores. No model judge or calendar writes.', max_concurrency=1)
    rows = list(result)
    print(json.dumps({'dataset_id': str(dataset.id), 'experiment': result.experiment_name, 'cases': len(rows), 'outcomes': [r['run'].outputs for r in rows]}, indent=2))

if __name__ == '__main__':
    main()
