"""Run realistic free-calendar cases in LangSmith; no calendar or model calls."""
import json,hashlib
from pathlib import Path
from langsmith import Client
from simmer.domain import PlanInputs
from evaluate_realistic_gatherings import evaluate
ROOT=Path(__file__).resolve().parents[1]
def main():
 values=dict(l.split('=',1) for l in (ROOT/'.env.langsmith-evals').read_text().splitlines() if '=' in l)
 client=Client(api_key=values['LANGSMITH_EVAL_API_KEY'])
 cases={c['id']:c for c in json.loads((ROOT/'evals/realistic-free-calendar-corrected.json').read_text())}
 name='simmer-realistic-free-calendar-v1'
 if client.has_dataset(dataset_name=name):dataset=client.read_dataset(dataset_name=name)
 else:
  dataset=client.create_dataset(name,description='20 realistic gatherings from 32 locally saved recipes; free simulated calendar, fixed daily budgets and buffers. No actual calendar access. Ingredient quantities and cooking execution still require separate review.')
  for c in cases.values():
   g=c['inputs']['gathering']
   client.create_example(dataset_id=dataset.id,inputs={'case_id':c['id'],'name':c['name'],'guests':g['guests'],'daily_limits':g['daily_limits'],'buffer_minutes':g['relax_minutes'],'menu':[s['title'] for s in c['inputs']['selections']]},outputs={'expected_outcome':'no_fit_found' if c['id']=='realistic-05' else 'complete'})
 def target(inputs):
  r=evaluate(PlanInputs.model_validate(cases[inputs['case_id']]['inputs']))
  return {k:r[k] for k in ('status','outcome','validator_codes','assignment_count','fit_days')}
 def valid(outputs):return {'key':'valid_complete_only','score':int(outputs['status']!='feasible' or not outputs['validator_codes'])}
 def expected(outputs,reference_outputs):return {'key':'expected_outcome','score':int(outputs['outcome']['code']==reference_outputs['expected_outcome'])}
 def completion(outputs):return {'key':'complete_plan','score':int(outputs['outcome']['code']=='complete')}
 experiment=client.evaluate(target,data=dataset.name,evaluators=[valid,expected,completion],experiment_prefix='realistic-free-calendar',max_concurrency=1,metadata={'fixture_sha256':hashlib.sha256((ROOT/'evals/realistic-free-calendar-corrected.json').read_bytes()).hexdigest()},description='After source-reviewed timing and vegetarian metadata corrections. One documented 45-minute freshness versus 60-minute buffer conflict is expected. Code evaluators, no LLM judge.')
 rows=list(experiment)
 print(json.dumps({'experiment':experiment.experiment_name,'dataset_id':str(dataset.id),'cases':len(rows)}))
if __name__=='__main__':main()
