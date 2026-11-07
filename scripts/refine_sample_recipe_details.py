import json,re,copy
from pathlib import Path
root=Path(__file__).resolve().parents[1]
s=copy.deepcopy(json.loads((root/'evals/fixtures/hosting-menus.json').read_text())[1])
notes={
'paneer-tikka':{'coat':'Cut paneer, peppers and onion into 1-inch pieces. Mix yogurt, spices, ginger, garlic and lemon juice; coat the pieces evenly.','cook':'Soak wooden skewers for 10 minutes. Alternate paneer and vegetables. Preheat at 400°F for 5 minutes; cook at 360°F for 5 minutes, turn, then cook 2–3 minutes more. Leave space between skewers; do not crowd the basket.'},
'palak-paneer-instant-pot':{'prep':'Finely chop the onion. Wash spinach. Blend cashews with milk until smooth. Green chili: use 1–2 tsp per original 4-serving recipe, to taste; shopping allows the upper end.','base':'Sauté cumin, ginger, garlic and chili for a minute; add onion for 2 minutes. Add spinach, water and salt. Pressure-cook on high: 0 minutes for fresh spinach, 1 minute for frozen. Quick-release.','blend':'Blend spinach until smooth, then stir in the cashew paste.','finish':'Add paneer and garam masala to the reheated sauce. Stir gently until hot throughout; avoid breaking the cubes.'},
'moms-veg-pulao':{'chop':'Slice onion thinly. Cut cauliflower into 1-inch florets, carrots into strips about 2 inches long and ¼ inch thick, and beans into diagonal 1-inch pieces.','vegetables':'Fry cashews until lightly golden and set aside. Cook onions until translucent. Sauté cauliflower until tender, then carrots and beans; add peas and corn last. Keep the fried cashews for garnishing.','rice':'Rinse and drain rice. Sauté whole spices in ghee, add rice and water, and bring to a boil. Cover and simmer on low for 10 minutes; uncover off the heat to let steam escape.','combine':'Fold hot vegetables gently into cooked rice so grains stay intact. Cover on low heat until hot throughout; finish with the reserved cashews.'},
'indian-cucumber-salad':{'chop':'Finely dice cucumbers and chop cilantro. Keep salt and sugar aside until serving to prevent a watery salad.','temper':'Heat ghee over medium heat. Sizzle crushed cumin for about 30 seconds, then add hing and the split chili for another 30 seconds.','finish':'Toss cucumber with the spiced ghee, peanuts and cilantro. Add salt and sugar just before serving.'},
'carrot-halwa-instant-pot':{'grate':'Peel and grate carrots; the original six-serving recipe uses about 6 packed cups.','pressure':'Sauté grated carrots in ghee for 2–3 minutes. Add almond milk; pressure-cook on high for 5 minutes, then quick-release.','reduce':'Stir in sugar, almond meal, cardamom, raisins and saffron. Sauté 5–7 minutes, stirring frequently, until most liquid evaporates. It thickens further as it cools.','serve':'Garnish with sliced almonds or pistachios. Serve chilled or warm, as preferred.'}}
corrections=[]
for sel in s['inputs']['selections']:
 r=sel['recipe'];slug=r['source'].rstrip('/').split('/')[-1]
 for ing in r['ingredients']:
  if ing['quantity'] is None:
   original=ing['name'];m=re.match(r'^(\d+) to (\d+) teaspoon (.+)',original)
   if m:ing.update(name=m[3]+' (to taste; shopping uses upper end)',quantity=float(m[2]),unit='tsp')
   else:
    m=re.match(r'^(\d+) (.+)',original);assert m,original
    ing.update(name=m[2],quantity=float(m[1]),unit='count')
   corrections.append({'recipe':r['title'],'source':r['source'],'original':original,'corrected':dict(ing)})
 for t in r['tasks']:
  if t['id'] in notes.get(slug,{}):t['guidance']=notes[slug][t['id']]
 for a in s['plan']['assignments']:
  if a['task']['recipe_id']==sel['id']:
   task=next((t for t in r['tasks'] if a['task']['title'].endswith(t['title'])),None)
   if task:a['task']['guidance']=task['guidance']
from simmer.domain import PlanInputs
from simmer.inventory import shopping_for
s['plan']['shopping']=[i.model_dump() for i in shopping_for(PlanInputs.model_validate(s['inputs']))]
assert not any(i['quantity'] is None for i in s['plan']['shopping'])
(root/'docs/reviews/2026-11-06-source-corrected-preview.json').write_text(json.dumps(s,indent=2)+'\n')
(root/'docs/reviews/2026-11-06-ingredient-corrections.json').write_text(json.dumps(corrections,indent=2)+'\n')
print(len(corrections),'source ingredient corrections; zero missing shopping quantities')
