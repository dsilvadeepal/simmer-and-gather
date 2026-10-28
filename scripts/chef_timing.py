"""One-time, human-authored home-cook estimates for the curated recipe collection.

A phase is [description, active_minutes, unattended_minutes]. Cleanup is separate.
These are planning guesses, not source instructions or tested times.
"""
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
rows=json.loads((ROOT/'docs/recipe-collection.json').read_text())
# Order matches the curated collection; explicit length and title are checked below.
PHASES=[
([('Cut paneer and vegetables; mix marinade',20,0),('Marinate in refrigerator',0,30),('Skewer and air-fry one batch',10,10)],10),
([('Cook and dice potatoes; prepare filling',25,15),('Prepare chutneys if needed',15,0),('Fill shells near serving',15,0)],10),
([('Mix marinade and coat wings',20,0),('Marinate in refrigerator',0,30),('Cook wings in batches',15,30)],10),
([('Measure and season nuts',5,0),('Roast and cool',5,20)],5),
([('Cut chicken and measure sauce ingredients',15,0),('Pressure cook and release',5,25),('Finish sauce',10,0)],10),
([('Measure sauce ingredients and prepare paneer',15,0),('Cook sauce and warm paneer',10,20)],10),
([('Soak chickpeas if using dried beans',5,180),('Chop aromatics and measure spices',20,0),('Pressure cook and finish curry',10,60)],10),
([('Rinse lentils and measure ingredients',15,0),('Pressure cook and release',5,50),('Finish with cream and seasoning',10,0)],10),
([('Wash/chop spinach and prepare paneer',20,0),('Cook, blend and finish sauce',15,15)],10),
([('Rinse rice and chop vegetables',25,10),('Saute vegetables and spices',10,0),('Cook rice and rest',5,25)],10),
([('Chop cucumber and herbs',10,0),('Mix dressing and combine',5,0)],5),
([('Wash herbs and measure ingredients',10,0),('Blend and adjust seasoning',5,0)],5),
([('Rinse rice and measure milk/sugar',10,0),('Pressure cook and release',5,35),('Stir and adjust texture',10,0)],10),
([('Grate carrots and measure ingredients',25,0),('Pressure cook and release',5,15),('Reduce while stirring',10,10)],10),
([('Measure ingredients and prepare pan',10,0),('Cook mixture while stirring',15,5),('Set, cut and portion',10,20)],10),
([('Prepare fish mixture and crumbs',20,0),('Shape and coat croquettes',15,0),('Fry in batches',20,20)],15),
(None,None),
(None,None),
([('Measure and grind curry paste',25,0),('Prepare protein/vegetables',15,0),('Cook curry and adjust seasoning',15,30)],15),
([('Prepare batter and fermentation vessel',20,0),('Ferment batter; duration depends on source and room',0,480),('Portion and steam in batches',15,30)],10),
([('Measure and cook coconut/lentil mixture',25,25),('Stir, shape and cool sweets',25,30)],15),
(None,None),
([('Mix cookie dough',20,0),('Shape and bake batches',15,25),('Cool and coat cookies',10,20)],10),
([('Cook apple filling',15,10),('Wrap brie and brush dough',10,0),('Bake and rest',5,35)],10),
([('Pit dates and prepare fillings',10,0),('Fill and arrange dates',20,0)],5),
([('Season turkey and prepare roasting pan',25,0),('Roast; monitor temperature and baste as needed',15,240),('Rest and carve',20,30)],20),
([('Peel/cut potatoes and garlic',15,0),('Boil until tender',5,25),('Mash and season',10,0)],10),
([('Prepare sweet potatoes and topping',25,0),('Cook/assemble casserole',15,30),('Bake',5,50)],15),
([('Make or cube cornbread and chop vegetables',45,0),('Saute aromatics and assemble stuffing',20,10),('Bake',5,40)],15),
([('Wash fruit and measure ingredients',10,0),('Simmer sauce',5,15),('Cool and refrigerate',0,30)],5),
([('Trim beans and prepare sauce/topping',25,0),('Cook and assemble casserole',15,20),('Bake',5,20)],15),
([('Trim and halve sprouts',15,0),('Roast or saute in batches',10,25)],10),
([('Make filling and prepare pie shell',30,0),('Bake and cool',5,85)],15),
([('Cook/mash sweet potatoes and make filling',45,20),('Fill crust and bake',10,60),('Cool before slicing',0,60)],15),
([('Peel and slice apples; mix topping',25,0),('Bake and rest',5,55)],10),
([('Cook/chop mushrooms and aromatics',25,10),('Mix, shape and coat cutlets',20,0),('Fry in batches',15,15)],15),
([('Cook/season filling and prepare binder',30,15),('Shape and coat cutlets',20,0),('Fry in batches',20,20)],15),
([('Cut pork and prepare spice blend',30,0),('Cook and stir bafat',15,40)],15),
(None,None),
([('Chop/soak fruit and measure cake ingredients',45,0),('Mix batter and prepare pan',15,0),('Bake and cool before slicing',5,60)],15),
]
assert len(rows)==len(PHASES)==40
out=[]
for row,(phases,cleanup) in zip(rows,PHASES):
    if phases is None:
        out.append({'title':row['title'],'url':row['url'],'basis':'insufficient source detail','phases':[],'cleanup_minutes':None,'active_minutes':None,'unattended_minutes':None,'elapsed_minutes':None,'review':'Find complete ingredients and directions before task-level estimate.'})
        continue
    active=sum(x[1] for x in phases)+cleanup
    unattended=sum(x[2] for x in phases)
    review='Base recipe only; confirm servings, equipment batches, and real pace before scheduling.'
    if 'Sannas' in row['title']: review+=' Fermentation time is highly variable.'
    if 'Turkey' in row['title']: review+=' The listed bird is 14–16 lb; roast duration is a size-based planning allowance, not a doneness target. Cook to a measured safe internal temperature.'
    out.append({'title':row['title'],'url':row['url'],'basis':'chef estimate, untested','phases':[{'task':x[0],'active_minutes':x[1],'unattended_minutes':x[2]} for x in phases],'cleanup_minutes':cleanup,'active_minutes':active,'unattended_minutes':unattended,'elapsed_minutes':active+unattended,'review':review})
(ROOT/'docs/recipe-chef-timing.json').write_text(json.dumps(out,indent=2)+'\n')
print({'total':len(out),'estimated':sum(x['active_minutes'] is not None for x in out),'unknown':sum(x['active_minutes'] is None for x in out)})
