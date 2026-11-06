"""Conservative, repeatable library corrections; no gathering/calendar writes.
Source cache is populated separately. Run with --apply only after reviewing report.
"""
import json,re,sys,hashlib
from pathlib import Path
from sqlalchemy import select
from sqlalchemy.orm import Session
from simmer.models import Document
from simmer.domain import RecipeSnapshot,PrepTask
from simmer.hosting_recipe import hosting_readiness
from simmer.recipes import RecipeService

# Notes describe the selected method, rather than copying unrelated page variants.
NOTES={
0:{0:'Coat paneer, peppers and onion in the yogurt marinade. Refrigerate covered.',1:'Marinate for 30 minutes; the recipe permits refrigeration up to 24 hours.',2:'If using wooden skewers, soak them for 10 minutes while threading ingredients. Preheat the air fryer to 400°F for 5 minutes.',3:'Cook at 360°F for 5 minutes, turn and cook another 2–3 minutes. Check for hot centres and lightly browned edges; serve hot.'},
1:{1:'Cool potatoes before peeling and dicing. Sizzle cumin and fennel in oil, add ginger, spices and potatoes, then let the filling cool.',3:'Fill ready-made phyllo cups and bake at 325°F for about 15 minutes, until golden.',4:'Add yogurt, chutneys, sev, pomegranate and cilantro just before serving so the shells stay crisp.'},
2:{3:'Use the oven method: roast at 400°F until the thickest part reaches 165°F. Finish under the broiler for about 2 minutes, watching closely.'},
3:{1:'Bake at 300°F for 20 minutes, stirring every 5–7 minutes.',2:'Cool completely before sealing airtight.'},
4:{1:'Sauté onion until soft; add ginger, garlic and spices. Add tomato and the watery portion of coconut milk, reserving its cream. Stir in chicken.',2:'For chicken thighs: pressure-cook on high for 8 minutes, then quick-release following your cooker instructions. Check chicken is cooked through.',3:'Stir in reserved coconut cream, tomato paste, garam masala, fenugreek and seasoning. Simmer uncovered for about 5 minutes to thicken.'},
5:{1:'Sauté aromatics in the Instant Pot; add tomato and water. Pressure-cook on high for 8 minutes.',2:'Quick-release safely, then blend the sauce smooth.',3:'Stir in paneer, cream, tomato paste, fenugreek and sugar; simmer gently for about 5 minutes.'},
6:{2:'After soaking, drain chickpeas. Pressure-cook with the sautéed aromatics and water for 35 minutes on high, then allow natural release. Check tenderness.',3:'Add tomatoes after pressure cooking; simmer until softened. Add garam masala and cilantro.'},
7:{2:'Add drained soaked beans, tomato, spices and water. Pressure-cook on high for 30 minutes, followed by natural release. Check beans are tender.',3:'Stir in cream and garam masala; garnish. The optional pot-in-pot brown rice is not included in these dal-only tasks.'},
8:{1:'Sauté aromatics, then add spinach and water. Pressure-cook fresh spinach at 0 minutes on high (1 minute for frozen), then quick-release.',2:'Blend the spinach sauce, stir in cashew paste and paneer, and warm on sauté for about 2 minutes.'},
9:{1:'Rinse rice, sauté whole spices, add rice and water. Bring to a boil, cover and cook on low for 10 minutes. Uncover briefly while finishing vegetables.',2:'Fry cashews and reserve. Sauté onions, then cauliflower, beans and carrots in stages; add peas and corn last.',3:'Fold vegetables into rice gently. Cover and warm on low for 5–10 minutes; garnish with cashews.'},
10:{2:'Add tempering, cilantro and peanuts. Add salt and sugar only just before serving to avoid watery cucumber.'},
11:{4:'Roast at 450°F for 45 minutes, then reduce to 325°F. Check breast, thigh and wing joint all reach 165°F. Cooking duration varies with turkey size; use a thermometer.'},
13:{1:'Use the Porridge programme and allow natural pressure release. Check rice is soft before finishing.',3:'If serving chilled, cool promptly in shallow containers and refrigerate. If serving warm, keep hot until serving.'},
14:{1:'Pressure-cook grated carrots with almond milk on high for 5 minutes; quick-release.',2:'Add sugar, almond meal and spices. Sauté for 5–7 minutes, stirring frequently until thickened; it thickens further as it cools.'},
22:{2:'Bake at 120°C (248°F) for approximately 2½–3 hours. Check with a skewer; shield the top if browning too quickly.',3:'Rest in the tin about 20 minutes, then turn out and cool completely before wrapping airtight.'},
24:{1:'Toast pecans at 350°F for 6–8 minutes, watching closely, then cool.',3:'Brush pastry with egg wash and bake at 350°F for about 25 minutes until golden. Rotate the tray halfway.',4:'Rest for 10 minutes before slicing so the cheese does not run out immediately.'},
27:{0:'Roast sweet potatoes at 375°F until fork-tender, about an hour. Let cool enough to handle before peeling.',3:'Bake at 375°F until the topping is toasted and the casserole is hot, about 20 minutes.'},
28:{0:'Bake the cornbread at 425°F until a toothpick comes out clean, about 16–20 minutes.',1:'Cool cornbread before cubing; toast cubes at 300°F for 15 minutes.',2:'Cook sausage and vegetables, then let cool briefly before combining with the egg mixture.',3:'Combine with broth and eggs and bake at 375°F for 35–40 minutes. Cool promptly and refrigerate if preparing ahead.',4:'Reheat covered at 350°F until the centre reaches 165°F; uncover briefly to crisp the top. Reheating allowance is an estimate.'},
29:{2:'Let the sauce cool, then cover and refrigerate; serve chilled or at room temperature.'},
30:{3:'Broil in a broiler-safe dish, watching constantly, for 1–3 minutes until browned and bubbling. Rest for 10 minutes.'},
32:{2:'Blind-bake at 375°F with weights for 25 minutes, then without weights for 5–10 minutes; let cool.',3:'Melt chocolate and butter gently; cool slightly before adding eggs and the remaining filling ingredients.',4:'Bake at 375°F for 40–50 minutes until just set with a slight wobble in the centre.',5:'Cool completely. Cover and refrigerate once cool.'},
33:{4:'Bake at 375°F for 10 minutes, then reduce to 325°F for about 50 minutes until set. Shield the crust if it browns too quickly.',5:'Cool completely before slicing. Keep whipped cream refrigerated and add when serving.'},
34:{2:'Bake at 350°F until the topping is golden and the apples are tender. Let rest before serving.'},
35:{0:'Boil or pressure-cook potato until tender, drain promptly and mash; avoid a waterlogged mixture.',1:'Cook chopped mushrooms until excess liquid evaporates. Sauté onion and aromatics, then combine with mushrooms and spices.',2:'Cool until comfortable to handle, mix with mashed potato and crumbs, then shape. Add crumbs only as needed for a soft but non-sticky mixture.',3:'Coat with crumbs and pan-fry on medium heat until golden on both sides. Stay at the pan; serve hot.'},
}
TEMPS={0:{2:400,3:360},1:{3:325},2:{2:400,3:400},3:{1:300},11:{4:450},22:{2:248},24:{1:350,3:350},27:{0:375,3:375},28:{0:425,1:300,3:375,4:350},32:{2:375,4:375},33:{4:375},34:{2:350}}

def refine(r,n,source):
 r=r.model_copy(deep=True); changes=[]
 if source and source.get('tasks'):
  r.preparation_provenance['source_method_text']='\n'.join(t['title'] for t in source['tasks'])
  if any('cooking instructions' in x.name.lower() for x in r.ingredients):
   from simmer.domain import Ingredient
   r.ingredients=[Ingredient.model_validate(x) for x in source['ingredients']];changes.append('Replaced import placeholder with source ingredients')
 for j,t in enumerate(r.tasks):
  if t.eligible:t.eligible=None;changes.append('Removed test-specific dates')
  if t.preparation_policy=='unknown':
   t.preparation_policy='same_day';t.max_ahead_hours=None;changes.append('Same-day default where advance storage is unverified')
  if j in NOTES.get(n,{}):t.guidance=NOTES[n][j];changes.append('Step-specific instructions')
  if j in TEMPS.get(n,{}):t.temperature=TEMPS[n][j];changes.append('Cooking temperature')
  if t.minutes and t.active_minutes is None:t.active_minutes=0 if t.unattended else t.minutes
  if t.presence_minutes is None:t.presence_minutes=t.active_minutes
  if re.search(r'pan.fry|shallow.fry|deep.fry',t.title,re.I):t.presence_minutes=t.minutes;t.unattended=False;changes.append('Continuous frying supervision')
  if t.minutes and 0<(t.active_minutes or 0)<t.minutes and not t.attention_segments:
   t.presence_minutes=t.minutes
  if n in (4,5,6,7,8,13,14) and re.search('pressure',t.title,re.I):t.resource='instant_pot'
 # Remove repeated recipe-wide prose from individual task instructions.
 for t in r.tasks:
  if t.guidance and re.search(r'Cook fully 1 day ahead|Cook sauce 1 day ahead|cook curry 1 day ahead|Home-cook|Method reviewed',t.guidance):
   t.guidance=None
 if n==9:r.tasks[1].guidance+=' Let steam escape briefly; do not leave cooked rice out for prolonged cooling.'
 if n==15:r.tasks[-1].guidance='Cool until set before cutting; pack airtight.'
 if n==26:r.tasks[2].guidance+=' Cool promptly in shallow containers before refrigerating.'
 if n==33:r.tasks[-1].guidance+=' Cover and refrigerate after cooling.'
 if n==33:r.tasks[0].guidance='Roll crust, fit into the dish, cover and refrigerate at least 30 minutes.'
 if not source or not source.get('tasks'):
  # Prior manually reviewed excerpts are not a machine-readable method.
  # Do not search unrelated boilerplate for mandatory recipe steps.
  r.preparation_provenance['source_method_text']=(r.source_text.split('Preparation review ·')[-1].split('Timing and scaling notes:')[0] if 'Preparation review ·' in r.source_text else r.source_text.split('Home-cook timing draft')[0])
  r.uncertainties=list(dict.fromkeys(r.uncertainties+['Structured source method unavailable; retain manual source review and verify detailed instructions before a new menu.']))
 if n==19:r.tasks[0].guidance='Soak tamarind in warm water while preparing the coconut extract. '+(r.tasks[0].guidance or '')
 if n==23:
  r.reviewed=False
  r.uncertainties=list(dict.fromkeys(r.uncertainties+['Verify cookie baking temperature; pecan toasting temperature is not sufficient evidence.']))
 if n==1:r.tasks[3].resource='oven' 
 if n==7:r.title='Instant Pot Dal Makhani' # optional rice not actually planned
 # Separate setup from overnight waits without changing downstream dependency IDs.
 out=[]
 for t in r.tasks:
  if re.search(r'soak',t.title,re.I) and (t.active_minutes or 0)>0 and t.minutes>60:
   setup=t.model_copy(deep=True);setup.id=t.id+'-setup';setup.title='Rinse beans and cover with water';setup.minutes=t.active_minutes;setup.presence_minutes=t.active_minutes;setup.attention_segments=[]
   setup.preparation_policy='advance';setup.max_ahead_hours=24;setup.storage_anchor='next_step';setup.guidance='Rinse beans and cover generously with water. Drain after soaking.'
   t.minutes-=t.active_minutes;t.active_minutes=0;t.presence_minutes=0;t.unattended=True;t.attention_segments=[];t.dependencies=[setup.id];t.title='Soak beans overnight';t.preparation_policy='advance';t.max_ahead_hours=24;t.storage_anchor='next_step'
   out.append(setup);changes.append('Separated soaking setup and passive wait')
  out.append(t)
 r.tasks=out
 if n==0:
  for t in r.tasks[:2]:t.preparation_policy='advance';t.max_ahead_hours=24;t.storage_anchor='next_step'
 if n==25:
  r.uncertainties=list(dict.fromkeys(r.uncertainties+['Choose one stuffed-date filling before scheduling; the source contains six different variants and allergens.']))
  r.reviewed=False
 r.preparation_provenance['library_audit']='2026-10-29; source methods checked; unverified advance windows default to same day; no saved-plan updates'
 return r,list(dict.fromkeys(changes))

def protected_snapshot(store,owner):
 with Session(store.engine) as session:
  rows=session.scalars(select(Document).where(Document.owner==owner,Document.kind!='recipe')).all()
  return {f'{r.kind}/{r.id}':hashlib.sha256(json.dumps({'body':r.body,'revision':r.revision},sort_keys=True).encode()).hexdigest() for r in rows}
