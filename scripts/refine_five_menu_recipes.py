"""Reviewed logical splits for the five-menu rerun; pure transformations only.

Timing and attention placement are home-cook estimates. Source-supported storage
is distinguished from conservative culinary estimates in provenance. No writes.
"""
from simmer.domain import PrepTask,AttentionSegment

def task(id,title,elapsed,active=None,*,deps=(),ahead=48,resource=None,note='',checks=None,temp=None,anchor='serving'):
    active=elapsed if active is None else active
    return PrepTask(id=id,title=title,minutes=elapsed,active_minutes=active,presence_minutes=active,
        dependencies=list(deps),resource=resource,temperature=temp,max_ahead_hours=ahead,
        preparation_policy='advance' if ahead is not None else 'same_day',storage_anchor=anchor,
        unattended=active==0,scale_mode='combined',guidance=note,
        attention_segments=[AttentionSegment(offset_minutes=o,minutes=m) for o,m in (checks or [])],
        evidence='Reviewed publisher method; timing/check-ins are home-cook estimates. See recipe preparation provenance.',timing_basis='estimate')

def cool(dep,ahead=48):
    return task('store','Portion, cool promptly and refrigerate',10,deps=[dep],ahead=ahead,note='Transfer to shallow containers and refrigerate promptly. Do not wait for the whole pot to cool on the counter.')
def reheat(dep,resource='stovetop'):
    return task('reheat','Reheat gently and keep hot',25,10,deps=[dep],ahead=2.5,resource=resource,checks=[(0,5),(20,5)],note='Stir and heat through to 165°F; add a splash of water if needed. Keep at 140°F or above until serving. Stay nearby for checks.')

def refine(recipe):
 r=recipe.model_copy(deep=True);name=r.title.lower();basis='Conservative 24–48 hour refrigerated component allowance is a culinary planning estimate, not a publisher-tested claim.'
 if 'aloo chaat' in name:
  r.tasks=[task('potato','Steam potatoes',35,5,resource='instant_pot',checks=[(0,5)],note='Steam until tender and allow pressure to release safely.'),task('filling','Cool briefly, dice potatoes and sauté the filling',40,25,deps=['potato'],resource='stovetop',checks=[(15,25)],note='Let potatoes cool enough to handle, peel and dice. Sauté cumin, fennel, ginger and spices; fold in potatoes.'),cool('filling'),task('toppings','Prepare yogurt and chutneys; refrigerate separately',10,ahead=24,note='Use the recipe’s ready-made chutneys; whisk the yogurt sauce. Keep garnishes separate.'),task('bake','Fill phyllo shells and bake',25,10,deps=['store'],ahead=1.5,resource='oven',temp=325,checks=[(0,5),(20,5)],note='Fill shells with potato mixture; bake at 325°F until hot and golden, about 15 minutes.'),task('finish','Add chilled sauces and garnish the chaat cups',10,deps=['bake','toppings'],ahead=.75,note='Add yogurt, chutneys, sev, pomegranate and cilantro close to serving. Keep sauces chilled until this step.')]
  basis='Publisher explicitly permits potato filling ahead and yogurt the day before; 48 hours used for cooked filling. Final topping held close to serving.'
 elif 'butter chicken' in name:
  r.tasks=[task('prep','Cut chicken and chop aromatics',20,note='Cut chicken evenly; chop onion, ginger and garlic. Separate coconut cream from its watery portion.'),task('saute','Sauté aromatics; add tomato and chicken',15,deps=['prep'],resource='instant_pot',note='Soften onion, cook spices, then add tomato, coconut water and chicken.'),task('pressure','Pressure-cook and release safely',30,5,deps=['saute'],resource='instant_pot',checks=[(25,5)],note='For thighs, pressure-cook on high for 8 minutes then quick-release. Allow time to reach pressure; check chicken is cooked through.'),task('finish','Stir in coconut cream and finish sauce',10,deps=['pressure'],resource='instant_pot',note='Add reserved cream and finishing spices; simmer to thicken.'),cool('finish'),reheat('store')]
  basis='Publisher permits refrigerated leftovers up to five days; plan uses a shorter 48-hour cooked storage allowance, explicit cooling and reheating.'
 elif 'palak paneer' in name:
  r.tasks=[task('prep','Wash spinach, chop aromatics and blend cashew paste',20,ahead=24,note='Blend cashews and milk smooth; keep chilled. Wash spinach and chop onion, ginger and garlic.'),task('base','Sauté aromatics and pressure-cook spinach',20,10,deps=['prep'],ahead=24,resource='instant_pot',checks=[(0,5),(15,5)],note='Sauté aromatics, add spinach and water. Fresh spinach: 0 minutes high pressure; frozen: 1 minute. Quick-release safely.'),task('blend','Blend spinach sauce and stir in cashew paste',10,deps=['base'],ahead=24,note='Blend the cooked spinach and stir in cashew paste; reserve paneer for serving day.'),cool('blend',24),task('finish','Reheat spinach sauce; add paneer and season',20,15,deps=['store'],ahead=1.5,resource='stovetop',checks=[(0,10),(15,5)],note='Heat sauce thoroughly, stir in paneer and garam masala, and warm gently without overcooking the paneer. Keep hot until serving.')]
 elif 'vegetable pulao' in name:
  r.tasks=[task('chop','Chop the pulao vegetables',25,note='Cut vegetables to similar sizes for even cooking.'),task('vegetables','Fry cashews and sauté vegetables in stages',25,deps=['chop'],resource='stovetop',note='Reserve toasted cashews separately. Sauté onions and vegetables in stages; leave them slightly firm.'),cool('vegetables'),task('rice','Cook rice with whole spices',30,10,ahead=1.5,resource='stovetop',checks=[(0,5),(25,5)],note='Rinse rice, sauté whole spices, add water and simmer covered. Let steam escape briefly.'),task('combine','Reheat vegetables and fold into fresh rice',15,10,deps=['rice','store'],ahead=1,resource='stovetop',checks=[(0,5),(10,5)],note='Reheat the vegetables thoroughly, fold gently into rice, warm through and garnish with reserved cashews. Keep hot.')]
  basis='Publisher explicitly supports chopping and sautéing vegetables up to two days ahead, cooking rice on serving day.'
 elif 'carrot halwa' in name:
  r.tasks=[task('grate','Peel and grate carrots',20,note='Grate carrots evenly.'),task('pressure','Sauté carrots and pressure-cook with almond milk',25,10,deps=['grate'],resource='instant_pot',checks=[(0,5),(20,5)],note='Sauté briefly; pressure-cook with almond milk on high for 5 minutes, then quick-release.'),task('reduce','Add sugar and almond meal; stir until thick',15,deps=['pressure'],resource='instant_pot',note='Stir frequently to prevent sticking. Add spices; the mixture thickens as it cools.'),cool('reduce'),task('serve','Portion chilled halwa and refrigerate',10,deps=['store'],ahead=48,note='Portion, garnish and refrigerate covered. Serve chilled; no reheating required.')]
 elif 'paneer tikka' in name:
  r.tasks=[task('coat','Cut paneer and vegetables; coat in marinade',20,ahead=24,anchor='next_step',note='Mix yogurt marinade and coat paneer, peppers and onion. Refrigerate covered.'),task('marinate','Refrigerate to marinate',30,0,deps=['coat'],ahead=24,anchor='next_step',note='At least 30 minutes; the publisher permits up to 24 hours refrigerated.'),task('cook','Thread skewers, preheat and air-fry paneer tikka',30,15,deps=['marinate'],ahead=1,resource='air_fryer',temp=360,checks=[(0,10),(20,5)],note='Soak wooden skewers while preheating. Preheat at 400°F, then cook at 360°F, turning halfway, until hot and lightly charred. Keep warm briefly; texture is best fresh.')]
 elif 'cucumber salad' in name:
  r.tasks=[task('chop','Dice cucumber and chop cilantro; refrigerate',15,ahead=12,note='Keep covered and chilled; leave salt and sugar out until final assembly.'),task('temper','Sizzle spices for the cucumber salad',5,ahead=1.5,resource='stovetop',note='Sizzle cumin, hing and chilli in ghee; let cool briefly.'),task('finish','Toss cucumber salad with tempering and seasoning',5,deps=['chop','temper'],ahead=.75,note='Add tempering, peanuts, cilantro, salt and sugar. Keep chilled until serving; add seasoning as late as this prep window allows.')]
 elif 'apple crisp' in name:
  r.tasks=[task('assemble','Slice apples, mix topping and assemble crisp',35,note='Layer apples and topping in the baking dish; bake promptly after assembling.'),task('bake','Bake apple crisp until tender and golden',60,10,deps=['assemble'],resource='oven',temp=350,checks=[(0,5),(55,5)],note='Bake at 350°F; check apples are tender and topping golden.'),task('cool','Cool the apple crisp',60,0,deps=['bake'],note='Let cool before covering; refrigerate within two hours.'),task('store','Cover and refrigerate the crisp',5,deps=['cool'],note='Cover once cool and refrigerate.'),task('reheat','Rewarm the apple crisp',30,5,deps=['store'],ahead=2,resource='oven',temp=350,checks=[(25,5)],note='Rewarm at 350°F until hot. Serve warm, or allow to cool slightly while dinner is served.')]
  basis='Publisher supports refrigerating baked crisp up to four days and reheating at 350°F; plan uses 48 hours.'
 elif 'mushroom cutlets' in name:
  r.tasks=[task('potato','Boil and mash potato',35,10,ahead=24,resource='stovetop',checks=[(0,5),(30,5)],note='Drain promptly when tender; mash without excess water.'),task('filling','Cook mushrooms dry and sauté aromatics',25,ahead=24,resource='stovetop',note='Cook off mushroom moisture, then combine with sautéed onion, herbs and spices.'),task('cool','Let filling cool enough to handle',20,0,deps=['filling'],ahead=24,note='Cool briefly before shaping.'),task('shape','Mix, shape cutlets and refrigerate',25,deps=['potato','cool'],ahead=24,note='Mix with potato and crumbs. Shape and refrigerate covered; add crumbs only as needed.'),task('fry','Coat and pan-fry cutlets',25,deps=['shape'],ahead=1,resource='stovetop',note='Fry on medium heat until golden on both sides and hot throughout. Stay at the pan.')]
 elif 'black chana' in name:
  r.tasks=[task('rinse','Rinse chana and cover with water',5,ahead=1,anchor='next_step',note='Rinse and cover generously with water.'),task('soak','Soak chana overnight',720,0,deps=['rinse'],ahead=12,anchor='next_step',note='Soak for 10–12 hours in the refrigerator, then drain.'),task('pressure','Pressure-cook chana until tender',60,10,deps=['soak'],resource='instant_pot',checks=[(0,5),(55,5)],note='Cook until tender and allow pressure to release safely; appliance and bean age affect time.'),task('finish','Temper aromatics and finish chana sukka',40,deps=['pressure'],resource='stovetop',note='Chop onion and garlic, temper mustard and curry leaves, then add coconut, spices, chana and tamarind; simmer until absorbed.'),cool('finish'),reheat('store')]
 elif 'tuna croquettes' in name:
  r.tasks=[task('mix','Mix tuna filling',15,ahead=24,note='Drain canned tuna well; mix with chopped aromatics and the recipe binders.'),task('shape','Shape, coat and refrigerate croquettes',20,deps=['mix'],ahead=24,note='Shape and coat; refrigerate covered until cooking.'),task('cook','Air-fry croquettes, turning halfway',20,10,deps=['shape'],ahead=1,resource='air_fryer',temp=356,checks=[(0,5),(15,5)],note='Air-fry at 180°C (356°F), turning, until golden and hot through. Check the egg-bound filling is fully cooked.')]
 elif 'cafreal' in name:
  # Keep reviewed marinade and fresh cooking, but bound the waiting chain.
  r.tasks[0].storage_anchor='next_step';r.tasks[0].max_ahead_hours=1
  r.tasks[1].storage_anchor='next_step';r.tasks[1].max_ahead_hours=24
  r.tasks[-1].max_ahead_hours=1.5
 elif 'pork bafat' in name:
  for t in r.tasks:
   if t.preparation_policy=='advance':t.max_ahead_hours=48
  r.tasks[-1].max_ahead_hours=1.5
 elif 'sannas' in name:
  soaking=next(t for t in r.tasks if 'soak' in t.title.lower())
  grinding=next(t for t in r.tasks if 'grind' in t.title.lower())
  drained=task('drain','Drain soaked rice and refrigerate until grinding',5,deps=[soaking.id],ahead=4,anchor='next_step',note='Drain the soaked rice, cover and refrigerate until grinding later this morning. This short refrigerated hold is a planning estimate.')
  drained.max_dependency_gap_minutes=60
  grinding.dependencies=[drained.id]
  if not any(t.id=='drain' for t in r.tasks):r.tasks.insert(r.tasks.index(grinding),drained)
  for t in r.tasks:
   if t.active_minutes==0:t.storage_anchor='next_step';t.max_ahead_hours=.5 if 'rise' in t.title.lower() or 'ferment' in t.title.lower() else 12
  r.tasks[-1].max_ahead_hours=1.5
 elif 'doce' in name:
  for t in r.tasks:
   if 'soak' in t.title.lower() or 'rinse' in t.title.lower():t.storage_anchor='next_step';t.max_ahead_hours=12
  r.tasks[-1].guidance=(r.tasks[-1].guidance or '')+' Once cool, pack covered and refrigerate; remove portions shortly before serving.'
 elif 'mashed potatoes' in name or 'cornbread stuffing' in name:
  if 'mashed potatoes' in name:
   first=r.tasks[0];boil=r.tasks[1]
   boil.max_dependency_gap_minutes=15
   first.guidance=(first.guidance or '')+' Start boiling promptly after cutting.'
  else:
   first=r.tasks[0];cube=next(t for t in r.tasks if 'cube' in t.title.lower())
   cooled=task('cornbread-cool','Cool cornbread on a rack',60,0,deps=[first.id],ahead=48,note='Let cool fully before packing.');cooled.max_dependency_gap_minutes=0
   packed=task('cornbread-pack','Pack cooled cornbread airtight',5,deps=[cooled.id],ahead=48,note='Pack fully cooled cornbread at room temperature. The source permits up to two days.');packed.max_dependency_gap_minutes=15
   cube.dependencies=[packed.id];cube.title='Cube and toast the cornbread'
   if not any(t.id=='cornbread-cool' for t in r.tasks):r.tasks[1:1]=[cooled,packed]
  finish=r.tasks[-1]
  if not any(t.id=='store' for t in r.tasks):
   preceding=r.tasks[-2]
   storage=cool(preceding.id)
   r.tasks.insert(-1,storage);finish.dependencies=['store']
  finish.max_ahead_hours=2.5
  if 'mashed potatoes' in name:r.tasks[2].max_dependency_gap_minutes=15
  finish.guidance=(finish.guidance or '')+' Reheat to 165°F and keep hot until serving.'
  basis='Publisher explicitly supports preparing ahead and reheating; retain cooling and refrigeration as a scheduled step.'
 elif 'thanksgiving turkey' in name:
  for t in r.tasks:
   if t.active_minutes==0:t.storage_anchor='next_step';t.max_ahead_hours=24
   if 'roast' in t.title.lower() and t.resource=='oven':t.max_ahead_hours=2
  r.uncertainties=list(dict.fromkeys(r.uncertainties+['This plan requires a thawed turkey before brining; thawing a frozen turkey may need earlier refrigerator days.']))
 else:return None
 for t in r.tasks:
  if 'soak' in t.title.lower() and t.active_minutes==0:
   t.storage_anchor='next_step';t.max_ahead_hours=1
   t.guidance=(t.guidance or '')+' Keep refrigerated during the soak; continue with cooking or grinding when it finishes.'
  if 'dry-brining' in t.title.lower():t.max_ahead_hours=12
  if 'mushroom cutlets' in name and t.id=='shape':t.max_dependency_gap_minutes=15
  if 'mushroom cutlets' in name and t.id=='potato':t.guidance+=' Refrigerate promptly if the filling is not ready.'
  if t.dependencies and t.active_minutes==0:t.max_dependency_gap_minutes=0
  if 'reheat' in t.id or ('palak paneer' in name and t.id=='finish'):
   t.min_dependency_gap_minutes=180
  if 'aloo chaat' in name and t.id=='filling':t.max_dependency_gap_minutes=15
  if t.dependencies and not t.min_dependency_gap_minutes and t.id in ('saute','pressure','finish','blend','store','filling','shape','bake','cool') and t.id not in ('reheat',):
   # Preserve hot-food and batter transitions; raw/prepared components retain their explicit storage windows.
   if t.id in ('store','cool') or (t.id in ('pressure','finish','blend') and t.preparation_policy=='advance') or ('apple crisp' in name and t.id=='bake'):
    t.max_dependency_gap_minutes=15
 if any(x in name for x in ('sannas','doce','mushroom cutlets','palak paneer','paneer tikka','vegetable pulao','carrot halwa','cucumber salad','aloo chaat','black chana','apple crisp','mashed potatoes')):r.vegetarian=True
 if 'cafreal' in name:r.allergens=['milk']
 if 'sannas' in name:r.allergens=[]
 if 'doce' in name:r.allergens=['milk']
 if any(x in name for x in ('cafreal','sannas','doce')):
  r.preparation_provenance['ingredient_allergen_review']='Listed ingredients reviewed for gluten, peanuts and tree nuts; coconut retained. Package labels and cross-contact remain unverified.'
 r.preparation_provenance['make_ahead_rerun']='2026-10-29: '+basis
 return r
