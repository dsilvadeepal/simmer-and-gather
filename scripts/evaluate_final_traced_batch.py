"""20 seeded end-to-end planning runs under an isolated test owner; no calendar API."""
import os,json,random,hashlib
from pathlib import Path
from datetime import datetime,timedelta
from zoneinfo import ZoneInfo
from uuid import uuid4
from sqlalchemy import select
from sqlalchemy.orm import Session
from langsmith import Client
from simmer.domain import *
from simmer.db import Store
from simmer.models import Document
from simmer.recipes import RecipeService
from simmer.profiles import HostingService
from simmer.agent import PlanningService
from simmer.scheduler import validate_schedule
from simmer.alternatives import suggest_alternatives
ROOT=Path(__file__).resolve().parents[1]
def main():
 cfg=dict(os.environ)
 for name in ('.env.google','.env.notion','.env.services','.env.langsmith-evals'):
  for line in (ROOT/name).read_text().splitlines():
   if '=' in line and not line.startswith('#'):
    k,v=line.split('=',1);cfg[k]=v.strip().strip('"').strip("'")
 source_store=Store(cfg['DATABASE_URL']);realowner=cfg['ALLOWED_OWNER_ID']
 store=Store('postgresql+psycopg://simmer:local-dev-only@localhost:55444/simmer_final_check_20261107');store.create_schema()
 def fingerprint():
  with Session(source_store.engine) as session:
   rows=[(r.kind,r.id,r.revision,r.body) for r in session.scalars(select(Document).where(Document.owner==realowner))]
  return hashlib.sha256(json.dumps(sorted(rows,key=lambda x:(x[0],x[1])),sort_keys=True).encode()).hexdigest()
 before=fingerprint();library=RecipeService(source_store).list_recipes(realowner)
 def get(part):
  rows=[r for r in library if part.lower() in r.title.lower()];assert len(rows)==1,(part,len(rows));return rows[0]
 pools=[(['Butter Chicken','Chana Masala','Butter Paneer','Palak Paneer'],['Brussels','Vegetable Pulao','Black Chana'],['Rice Pudding','Carrot Halwa']),(['Cafreal','Pork Bafat','Vindaloo'],['Mashed Potatoes','Brussels','Black Chana'],['The Best Doce','Coffee Fruit Cake']),(['Thanksgiving Turkey','Butter Chicken'],['Mashed Potatoes','Cranberry Orange','Green Bean Casserole'],['Sweet Potato Pie','Apple Crisp'])]
 rng=random.Random(20261108);cases=[]
 for n in range(20):
  pool=pools[n%3];parts=[rng.choice(p) for p in pool];guests=rng.choice([4,6,8,10,12,15,16]);days=rng.choice([2,3,4]);budget=rng.choice([90,120,180,240]);buffer=rng.choice([30,60]);veg=0;allergies=[]
  arrival=datetime(2027,6,5,17,tzinfo=ZoneInfo('America/New_York'))+timedelta(days=n*7)
  dates=[(arrival-timedelta(days=k)).date() for k in reversed(range(days))]
  g=Gathering(id=f'final-traced-{n+1:02}',title=f'Sample gathering {n+1:02}',arrival=arrival,earliest_prep=dates[0],prep_days=dates,daily_limits={str(d):budget for d in dates},guests=guests,vegetarian_guests=veg,allergies=allergies,relax_minutes=buffer,finishing_minutes=0,category_counts={k:0 for k in ['starters','mains','sides','desserts','drinks']})
  expected='complete'
  if n in (3,7,11):
   start=(arrival-timedelta(days=1)).replace(hour=10)
   g.profile.helpers=[Helper(id='helper',name='Sample helper',skills=['cook'] if n!=11 else ['fetch'],supervision=n==11,available=[Interval(start=start,end=start+timedelta(minutes=30 if n==3 else 60))])]
  if n==14:parts=['Butter Chicken','Chana Masala','Carrot Halwa'];g.allergies=['gluten'];g.vegetarian_guests=2
  if n==15:parts=['Palak Paneer','Vegetable Pulao','Rice Pudding'];g.allergies=['nuts'];g.vegetarian_guests=guests;expected='needs_input'
  if n==16:parts=['Baked Brie','Cafreal','Mashed Potatoes'];g.allergies=['gluten'];expected='needs_input'
  if n==17:parts=['Butter Chicken','Tandoori chicken wings','Brussels'];g.vegetarian_guests=guests//2;expected='needs_input'
  if n==18:g.daily_limits={str(d):0 for d in dates};expected='no_fit_found'
  if n==19:g.allergies=None;expected='needs_input'
  selections=[MenuSelection(id=f'dish-{j}',title=get(p).title,category=get(p).category,recipe=get(p),servings=guests,vegetarian=get(p).vegetarian) for j,p in enumerate(parts)]
  busy=[]
  if n in (2,8,12):
   busy=[Interval(start=datetime.combine(d,datetime.min.time(),ZoneInfo('America/New_York')).replace(hour=12),end=datetime.combine(d,datetime.min.time(),ZoneInfo('America/New_York')).replace(hour=14)) for d in dates]
  data=PlanInputs(gathering=g,selections=selections,availability=AvailabilitySnapshot(status='fixture',busy=busy))
  cases.append({'id':g.id,'expected_outcome':expected,'inputs':data.model_dump(mode='json')})
 fixture=ROOT/'evals/final-traced-2026-11-07.json';fixture.write_text(json.dumps(cases,indent=2)+'\n')
 owner='eval-final-traced-'+str(uuid4());host=HostingService(store);planner=PlanningService(store)
 client=Client(api_key=cfg['LANGSMITH_EVAL_API_KEY'])
 from simmer.telemetry import Telemetry
 class RecordedTelemetry(Telemetry):
  def __init__(self):super().__init__(client,project='simmer-and-gather-dev',limit=100);self.ids=[]
  def record_run(self,*args,**kwargs):
   id=super().record_run(*args,**kwargs);self.ids.append(id);return id
 telemetry=RecordedTelemetry();planner=PlanningService(store,telemetry=telemetry)
 dataset=client.create_dataset('simmer-final-traced-'+owner[-8:],description='20 seeded gathering scenarios; real LangGraph planning service, isolated test owner, simulated availability (including three busy-window cases). No model judge.')
 for c in cases:client.create_example(dataset_id=dataset.id,inputs={'case_id':c['id']},outputs={'desired_outcome':c['expected_outcome']})
 rows=[];lookup={c['id']:c for c in cases}
 def target(inputs):
  c=lookup[inputs['case_id']];data=PlanInputs.model_validate(c['inputs'])
  g=host.save_gathering(owner,data.gathering,None);data.gathering=g
  store.put(owner,'inputs',g.id,data.model_dump(mode='json'))
  plan=planner.generate_final_plan(owner,g.id,g.revision,data.availability)
  checks=validate_schedule(data,plan)
  alternatives=suggest_alternatives(data,library) if c['id'] in ('final-traced-16','final-traced-17','final-traced-18') else None
  row={'id':c['id'],'expected':c['expected_outcome'],'outcome':plan.outcome.code,'valid_complete':plan.status!='feasible' or not checks,'violations':[v.model_dump() for v in plan.violations],'inputs':data.model_dump(mode='json'),'plan':plan.model_dump(mode='json'),'alternatives':alternatives}
  rows.append(row)
  print(c['id'],plan.outcome.code,'desired',c['expected_outcome'],flush=True)
  return {'outcome':plan.outcome.code,'valid_complete':row['valid_complete'],'alternative_count':len(alternatives['suggestions']) if alternatives else 0}
 def validity(outputs):return {'key':'valid_complete_only','score':int(outputs['valid_complete'])}
 def desired(outputs,reference_outputs):return {'key':'desired_outcome','score':int(outputs['outcome']==reference_outputs['desired_outcome'])}
 result=client.evaluate(target,data=dataset.name,evaluators=[validity,desired],experiment_prefix='final-traced',max_concurrency=1,metadata={'seed':20261108,'fixture_sha256':hashlib.sha256(fixture.read_bytes()).hexdigest()})
 list(result);assert fingerprint()==before
 (ROOT/'docs/reviews/2026-11-07-final-traced-results.json').write_text(json.dumps(rows,default=lambda x:x.model_dump(mode='json'),indent=2)+'\n')
 meta={'dataset_id':str(dataset.id),'experiment':result.experiment_name,'cases':len(rows),'real_owner_unchanged':True,'trace_ids':telemetry.ids,'seed':20261108,'calendar':'simulated availability: 17 free cases and 3 busy-window cases; no calendar integration calls'}
 (ROOT/'docs/reviews/2026-11-07-final-traced-run.json').write_text(json.dumps(meta,indent=2)+'\n');print(json.dumps(meta))
if __name__=='__main__':main()
