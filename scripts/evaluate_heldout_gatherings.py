"""Frozen second batch; evaluate without changing recipes, app records or calendars."""
import json
from pathlib import Path
from datetime import datetime,timedelta
from simmer.domain import *
from evaluate_realistic_gatherings import evaluate
ROOT=Path(__file__).resolve().parents[1]

def build():
 library={s['recipe']['title']:s['recipe'] for c in json.loads((ROOT/'evals/realistic-free-calendar-corrected.json').read_text()) for s in c['inputs']['selections']}
 names=list(library)
 def recipe(part):
  matches=[r for n,r in library.items() if part.lower() in n.lower()]
  assert len(matches)==1,(part,len(matches))
  return RecipeSnapshot.model_validate(matches[0])
 # Menus and expectations fixed before first execution. Complete is a hypothesis.
 specs=[
 ('Winter supper for four',['Butter Chicken','Brussels','Rice Pudding'],4,'2027-01-16',2,120,60,0,[],None,'complete'),
 ('Vegetarian weekday dinner',['Chana Masala','Butter Paneer','Carrot Halwa'],7,'2027-01-20',3,120,60,7,[],None,'complete'),
 ('Family Sunday roast',['Tandoori','Mashed','Cranberry','Apple Crisp'],9,'2027-01-24',3,180,60,0,[],None,'complete'),
 ('Goan birthday lunch',['Cafreal','Sannas','Doce'],14,'2027-02-06',3,180,30,0,[],None,'complete'),
 ('Vegetarian friends evening',['Paneer Tikka','Chana Masala','Rice Pudding'],6,'2027-02-13',3,120,60,6,[],None,'complete'),
 ('Winter holiday buffet',['Pork Bafat','Black Chana','Mashed','Fruit Cake Without'],16,'2027-02-20',4,180,30,0,[],None,'complete'),
 ('Spring daylight-saving supper',['Butter Chicken','Palak','Carrot Halwa'],8,'2027-03-14',3,150,60,3,[],None,'complete'),
 ('Fall daylight-saving supper',['Cafreal','Brussels','Rice Pudding'],11,'2027-11-07',3,150,60,0,[],None,'complete'),
 ('Dinner with adult helper',['Butter Chicken','Butter Paneer','Rice Pudding'],10,'2027-02-27',3,120,60,4,[],'adult120','complete'),
 ('Same dinner without helper',['Butter Chicken','Butter Paneer','Rice Pudding'],10,'2027-02-27',3,120,60,4,[],None,'complete'),
 ('Dinner with thirty-minute helper',['Chana Masala','Palak','Rice Pudding'],9,'2027-03-06',3,150,60,9,[],'adult30','complete'),
 ('Supervised helper weekend',['Tandoori','Mashed','Rice Pudding'],7,'2027-03-20',3,150,60,0,[],'supervised30','complete'),
 ('No nuts listed holiday meal',['Cafreal','Black Chana','Brussels','Doce'],13,'2027-04-03',4,180,30,0,['nuts'],None,'complete'),
 ('Gluten-screened curry dinner',['Butter Chicken','Chana Masala','Carrot Halwa'],5,'2027-04-10',3,180,60,2,['gluten'],None,'complete'),
 ('Potluck dessert contribution',['Butter Chicken','Butter Paneer','Brussels'],12,'2027-04-17',3,180,60,4,[],None,'complete'),
 ('Nut conflict in paneer meal',['Palak','Vegetable Pulao','Rice Pudding'],8,'2027-04-24',3,180,60,8,['nuts'],None,'needs_input'),
 ('Gluten conflict in holiday starter',['Baked Brie','Cafreal','Mashed'],8,'2027-05-01',3,180,30,0,['gluten'],None,'needs_input'),
 ('Vegetarian coverage missing',['Butter Chicken','Tandoori','Brussels'],10,'2027-05-08',3,180,60,5,[],None,'needs_input'),
 ('Zero prep allowance',['Butter Chicken','Rice Pudding'],4,'2027-05-15',2,0,60,0,[],None,'no_fit_found'),
 ('Allergies not confirmed',['Chana Masala','Brussels','Rice Pudding'],6,'2027-05-22',3,180,60,0,None,None,'needs_input'),
 ]
 # Brie not in previous 32: use saved local public recipe snapshot.
 for raw in json.loads(Path('/tmp/simmer-realistic-recipes.json').read_text()):
  if raw['title'] not in library:library[raw['title']]=raw
 from zoneinfo import ZoneInfo
 cases=[]
 for n,(title,parts,guests,day,days,budget,buffer,veg,allergies,helper,expected) in enumerate(specs,1):
  arrival=datetime.fromisoformat(day+'T18:00:00').replace(tzinfo=ZoneInfo('America/New_York'))
  dates=[(arrival-timedelta(days=k)).date() for k in reversed(range(days))]
  g=Gathering(id=f'heldout-{n:02}',title=title,occasion='Gathering',arrival=arrival,earliest_prep=dates[0],prep_days=dates,daily_limits={str(d):budget for d in dates},guests=guests,vegetarian_guests=veg,allergies=allergies,relax_minutes=buffer,finishing_minutes=0,category_counts={k:0 for k in ['starters','mains','sides','desserts','drinks']})
  if helper:
   duration=120 if helper=='adult120' else 30
   start=(arrival-timedelta(days=1)).replace(hour=10,minute=0)
   g.profile.helpers=[Helper(id='helper',name='Sample helper',skills=['cook'] if helper!='supervised30' else ['fetch','measure'],available=[Interval(start=start,end=start+timedelta(minutes=duration))],supervision=helper=='supervised30')]
  selections=[]
  for j,part in enumerate(parts):
   r=recipe(part);selections.append(MenuSelection(id=f'dish-{j}',title=r.title,category=r.category,recipe=r,servings=guests,vegetarian=r.vegetarian))
  if n==15:selections.append(MenuSelection(id='guest-dessert',title='Guest fruit platter',category='desserts',mode='guest',servings=12,vegetarian=True,contribution=Contribution(id='fruit',name='Fruit platter',person='Sample guest',servings=12,confirmed=True,warming_minutes=0)))
  data=PlanInputs(gathering=g,selections=selections,availability=AvailabilitySnapshot(status='fixture',busy=[]))
  cases.append({'id':g.id,'name':title,'expected_outcome':expected,'inputs':data.model_dump(mode='json')})
 return cases

def main():
 path=ROOT/'evals/heldout-gatherings-v1.json'
 if not path.exists():path.write_text(json.dumps(build(),indent=2)+'\n')
 cases=json.loads(path.read_text());rows=[]
 for c in cases:
  result=evaluate(PlanInputs.model_validate(c['inputs']))
  rows.append({'id':c['id'],'name':c['name'],'expected_outcome':c['expected_outcome'],'matches_expectation':c['expected_outcome']==result['outcome']['code'],**result})
  (ROOT/'docs/reviews/2026-11-07-heldout-results.json').write_text(json.dumps(rows,indent=2)+'\n')
  print(c['id'],c['name'],result['outcome']['code'],'expected',c['expected_outcome'],flush=True)
if __name__=='__main__':main()
