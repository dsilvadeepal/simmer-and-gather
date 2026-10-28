"""Curated chef planning proposals. Source claims and estimates remain separate."""
import json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
path=ROOT/'docs/recipe-collection.json';rows=json.loads(path.read_text())
# Counts are planning approximations for source cards without a usable serving yield.
SERVINGS={
'Easy Tuna Croquettes':(8,'chef estimate; 2 tuna cans, starter-size croquettes'),
'The Ultimate Goan Caldin Curry':(4,'chef estimate; 500 g fish'),
'Easy Traditional Goan Sannas':(12,'chef estimate; count of individual steamed cakes varies by mold'),
'The Best Doce':(24,'chef estimate; small sweet pieces, cut size varies'),
'Easy Christmas Fruit Cake Without Alcohol':(12,'chef estimate; 8-inch cake cut into 12 slices'),
'Super Easy Snowball Cookies':(18,'chef estimate; cookie size varies'),
'Coffee Fruit Cake':(10,'chef estimate; loaf/cake slice size varies'),
'Mushroom Cutlets':(8,'source yield, 8 medium cutlets'),
'Mince Meat Cutlets':(8,'source yield, 8 servings'),
'Pork Bafat | Dukra Maas':(4,'source yield, 4 people'),
'Cranberry Orange Sauce':(16,'chef estimate; approximately 2 cups at 2 tablespoons per condiment portion'),
'Stuffed Dates (6 Ways!)':(12,'publisher count of 12 dates; assumes one date per guest'),
}
# Prep guidance is deliberately conservative and describes quality as well as safe storage.
AHEAD={
'Tandoori chicken wings':'Mix yogurt marinade and coat wings the prior evening; refrigerate covered. Cook in batches near serving for crisp skin. Do not count unattended marination as active work.',
'Masala Nuts':'Roast and cool completely 1-2 days ahead; seal airtight only after cooling. Check crunch before serving; nuts are an explicit allergen.',
'Instant Pot Butter Chicken':'Cook fully 1 day ahead; divide into shallow containers and refrigerate promptly. Reheat thoroughly before serving; sauce usually tolerates this better than last-minute cooking.',
'Butter Paneer {Paneer Makhani}':'Cook sauce 1 day ahead and refrigerate promptly. Add or warm paneer close to serving to avoid rubbery texture; optional naan is separate and contains wheat unless a verified substitute is used.',
'Instant Pot Chana Masala (Punjabi Chole)':'Soak dried chickpeas as the source method requires; cook curry 1 day ahead and refrigerate promptly. Reheat thoroughly; check bean tenderness before relying on the planned cook time.',
'Instant Pot Palak Paneer':'Wash spinach and prepare sauce base 1 day ahead; refrigerate promptly. Finish with paneer near serving to protect texture and color. Contains cashews in the listed recipe.',
'Vegetable Pulao Recipe | Veg Pulav':'Wash/chop vegetables and measure spices 1 day ahead. Cook rice on party day, then hold hot or refrigerate promptly; rice quality drops if repeatedly warmed. Contains cashews in the listed recipe.',
'Indian Cucumber Salad (Kakdi Koshimbir)':'Wash cucumbers and prepare dressing components 1 day ahead, refrigerated separately. Chop/combine close to serving to avoid watery texture. Listed peanuts require allergy review.',
'Instant Pot Rice Pudding':'Cook fully 1 day ahead; cool promptly in shallow containers and refrigerate. Stir and adjust consistency before serving; serve chilled or reheat thoroughly if serving hot.',
'Easy Tuna Croquettes':'Mix and shape up to 1 day ahead; refrigerate covered. Fry close to serving for crispness; avoid a long warm hold. Tuna and bread crumbs are in the listed ingredients.',
'The Ultimate Goan Caldin Curry':'Make the spice/coconut curry base 1 day ahead and refrigerate. Add fish and finish cooking near serving to avoid overcooked fish; verify full cooking and seafood storage.',
'Easy Traditional Goan Sannas':'Start rice preparation and fermentation according to the source well before the party; fermentation varies with temperature. Steam 1 day ahead if needed, cool/refrigerate promptly, and re-steam near serving; test texture first.',
'The Best Doce':'Cook, shape and cool sweets 1 day ahead. Store covered according to ingredients and room conditions; choose refrigeration if uncertain. Large-batch stirring is hands-on and may exceed the current time estimate.',
'Super Easy Snowball Cookies':'Bake and cool 1-2 days ahead; store airtight. Roll/coating can be refreshed before serving if needed. Recipe lists wheat flour and pecans.',
'Thanksgiving Turkey':'For a 14-16 lb frozen bird, plan refrigerator thawing 3-4 days ahead. Season/brine per source before roasting; roast and rest early enough to protect the final hour. A whole turkey may need a simplified or bought alternative if oven capacity or schedule is tight.',
'Cranberry Orange Sauce':'Cook 1-2 days ahead; cool promptly and refrigerate covered. Serve chilled or bring to serving temperature as preferred.',
'Healthy Green Bean Casserole':'Trim/blanch beans and prepare sauce 1 day ahead; refrigerate separately. Assemble/bake on party day and keep crumb topping separate until near baking for texture.',
'Caramelized Brussels Sprouts':'Trim/halve sprouts and mix glaze 1 day ahead; refrigerate separately. Roast near serving for caramelization; reheating softens them.',
'Mushroom Cutlets':'Cook mushroom filling and shape cutlets up to 1 day ahead; refrigerate covered. Fry near serving for crispness and verify filling moisture.',
'Mince Meat Cutlets':'Cook meat filling fully and shape cutlets up to 1 day ahead; cool/refrigerate promptly. Fry near serving; verify the center is hot and the meat was safely cooked.',
'Pork Bafat | Dukra Maas':'Cook fully 1 day ahead; cool promptly in shallow containers and refrigerate. Reheat thoroughly. Flavor may deepen, but actual pork tenderness and batch size need checking.',
'Coffee Fruit Cake':'Bake 1-2 days ahead, cool completely before wrapping. Confirm the publisher storage advice and choose refrigeration/freezing if storing longer; nonalcoholic fruit cake is not a shelf-stable preserve.',
}
EQUIPMENT={
'Air Fryer Paneer Tikka':['Air fryer','Refrigerator'],
'Aloo Chaat in Phyllo Shells':['Stovetop','Refrigerator'],
'Tandoori chicken wings':['Oven','Refrigerator'],
'Masala Nuts':['Oven'],
'Instant Pot Butter Chicken':['Pressure cooker','Refrigerator'],
'Butter Paneer {Paneer Makhani}':['Stovetop','Refrigerator'],
'Instant Pot Chana Masala (Punjabi Chole)':['Pressure cooker','Refrigerator'],
'Instant Pot Dal Makhani with Brown Rice':['Pressure cooker','Refrigerator'],
'Instant Pot Palak Paneer':['Pressure cooker','Blender','Refrigerator'],
'Vegetable Pulao Recipe | Veg Pulav':['Stovetop','Refrigerator'],
'Indian Cucumber Salad (Kakdi Koshimbir)':['Stovetop','Refrigerator'],
'Cilantro Mint Chutney':['Blender','Refrigerator'],
'Instant Pot Rice Pudding':['Pressure cooker','Refrigerator'],
'Instant Pot Carrot Halwa Recipe':['Pressure cooker','Refrigerator'],
'Quick & Easy Badam Burfi (30 Minutes)':['Stovetop','Refrigerator'],
'Easy Tuna Croquettes':['Stovetop','Refrigerator'],
'Goan Pork Vindaloo':['Stovetop','Blender','Refrigerator'],
'Chicken Cafreal':['Stovetop','Blender','Refrigerator'],
'The Ultimate Goan Caldin Curry':['Stovetop','Blender','Refrigerator'],
'Easy Traditional Goan Sannas':['Stovetop','Blender','Refrigerator'],
'The Best Doce':['Stovetop','Refrigerator'],
'Easy Christmas Fruit Cake Without Alcohol':['Oven','Refrigerator'],
'Super Easy Snowball Cookies':['Oven'],
'Baked Brie En Croute':['Oven','Refrigerator'],
'Stuffed Dates (6 Ways!)':['Refrigerator'],
'Thanksgiving Turkey':['Oven','Refrigerator'],
'Garlic Mashed Potatoes Recipe':['Stovetop','Refrigerator'],
'Healthy Sweet Potato Casserole':['Oven','Stovetop','Refrigerator'],
'Cornbread Stuffing Recipe':['Oven','Stovetop'],
'Cranberry Orange Sauce':['Stovetop','Refrigerator'],
'Healthy Green Bean Casserole':['Oven','Stovetop','Refrigerator'],
'Caramelized Brussels Sprouts':['Oven','Refrigerator'],
'Chocolate Pecan Pie':['Oven','Refrigerator'],
'Sweet Potato Pie':['Oven','Stovetop','Refrigerator'],
'Gluten Free Apple Crisp':['Oven','Refrigerator'],
'Mushroom Cutlets':['Stovetop','Refrigerator'],
'Mince Meat Cutlets':['Stovetop','Refrigerator'],
'Pork Bafat | Dukra Maas':['Stovetop','Refrigerator'],
'Sonay Sukhe (Black Chana Sukka)':['Pressure cooker','Stovetop','Refrigerator'],
'Coffee Fruit Cake':['Oven','Stovetop','Refrigerator'],
}
assert len(rows)==len(EQUIPMENT)==40
assert set(AHEAD)=={r['title'] for r in rows if r['prep_evidence_status']=='Needs details'}
for r in rows:
 title=r['title'];base=SERVINGS.get(title)
 if base:
  r['estimated_base_servings'],r['base_servings_basis']=base
 else:
  match=re.search(r'\d+',str(r.get('yield_text') or ''))
  r['estimated_base_servings']=int(match.group()) if match else None
  r['base_servings_basis']='publisher recipe yield; confirm whether servings or individual pieces'
 r['equipment_assumption']=EQUIPMENT[title]
 r['equipment_review']='Confirm usable capacity, pot/pan size, number of batches and overlap with other dishes.'
 if title in AHEAD:
  r['chef_make_ahead_proposal']=AHEAD[title]
  r['make_ahead_basis']='Chef planning proposal, not publisher-confirmed storage window'
 else:
  r['chef_make_ahead_proposal']=None
  r['make_ahead_basis']='Publisher-specific note retained in prep_summary; confirm actual storage plan'
 r['planning_ready']=False
path.write_text(json.dumps(rows,indent=2)+'\n')
print({'servings_filled':sum(r['estimated_base_servings'] is not None for r in rows),'chef_make_ahead':len(AHEAD),'equipment_filled':len(EQUIPMENT)})
