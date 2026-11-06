"""Turn scoped Notion recipe notes into an editable, unreviewed planning draft."""
import re
from ..domain import Ingredient, PrepTask, RecipeSnapshot

UNIT=re.compile(r'^(\d+(?:[.,]\d+)?(?:\s+\d+/\d+|\s*[¼½¾⅓⅔⅛⅜⅝⅞])?|\d+/\d+|[¼½¾⅓⅔⅛⅜⅝⅞])\s*(cups?|tbsp|tablespoons?|tsp|teaspoons?|grams?|g|kg|ml|l|pounds?|lbs?|oz|cloves?|pieces?|cans?|count)\b\s*',re.I)
FRACTIONS={'¼':.25,'½':.5,'¾':.75,'⅓':1/3,'⅔':2/3,'⅛':.125,'⅜':.375,'⅝':.625,'⅞':.875}
STEP=re.compile(r'^(.+?):\s*(\d+)\s*min\s*(?:hands-on|active)(?:\s*\+\s*(\d+)\s*min\s*(?:waiting/cooking|waiting))?',re.I)
COURSES={'Starter':'starters','Main':'mains','Side':'sides','Dessert':'desserts','Drink':'drinks'}

def block_text(block):
    payload=block.get(block.get('type',''),{})
    return ''.join(x.get('plain_text',x.get('text',{}).get('content','')) for x in payload.get('rich_text',[])).strip()

def property_text(page,name):
    return ''.join(x.get('plain_text',x.get('text',{}).get('content','')) for x in page.get('properties',{}).get(name,{}).get('rich_text',[]))

def ingredient(line):
    line=line.strip(' •')
    match=UNIT.match(line)
    if not match:
        # Only parse explicit whole-item counts; do not treat unknown units as counts.
        count=re.match(r'^(\d+)\s+((?:(?:small|medium|large|raw|black|green|Indian|Persian)\s+)*(?:lemons?|peppers?|onions?|cashews?|bay leaf|peppercorns?|cardamom pods|carrots?|cucumbers?|chili)\b.*)$',line,re.I)
        if count: return Ingredient(name=count[2],quantity=float(count[1]),unit='count')
        return Ingredient(name=line)
    raw=match.group(1).replace(',','.')
    try:
        amount=0
        for token in raw.split():
            if '/' in token:
                numerator,denominator=token.split('/',1)
                amount+=float(numerator)/float(denominator)
            else:
                piece,fraction=re.fullmatch(r'(\d*(?:\.\d+)?)([¼½¾⅓⅔⅛⅜⅝⅞]*)',token).groups()
                amount+=(float(piece) if piece else 0)+sum(FRACTIONS[ch] for ch in fraction)
    except (ValueError,AttributeError,ZeroDivisionError): return Ingredient(name=line)
    unit=match.group(2).lower()
    unit={'tablespoon':'tbsp','tablespoons':'tbsp','teaspoon':'tsp','teaspoons':'tsp','cups':'cup','grams':'g','gram':'g','pounds':'lb','pound':'lb','lbs':'lb'}.get(unit,unit)
    return Ingredient(name=line[match.end():].strip() or line,quantity=amount,unit=unit)

def resource_for(title,equipment):
    text=title.casefold()
    if 'air-fry' in text or 'air fry' in text: return 'air_fryer'
    if 'pressure' in text: return 'instant_pot'
    if any(x in text for x in ('bake','roast','oven')) and 'Oven' in equipment: return 'oven'
    if any(x in text for x in ('fry','sauté','saute','simmer','boil','cook','temper','sear','reduce')) and 'Stovetop' in equipment: return 'stovetop'
    return None

def from_notion_details(page,blocks):
    props=page.get('properties',{})
    title=''.join(x.get('plain_text',x.get('text',{}).get('content','')) for x in props.get('Recipe',{}).get('title',[])) or 'Notion recipe'
    lines=[block_text(b) for b in blocks]
    ingredients=[]; collecting=False
    for line in lines:
        if line.startswith(('Ingredients (source facts','Ingredients (source quantities')):
            collecting=True; continue
        if collecting:
            if not line or line.startswith(('Cooking method','Home-cook timing','Source recipe:','Make-ahead:')): collecting=False
            else: ingredients.append(ingredient(line))
        if line.startswith(('Ingredients: ','Source ingredients: ')):
            ingredients.extend(ingredient(item) for item in line.split(': ',1)[1].split('; ') if item.strip())
    equipment={x.get('name') for x in props.get('Equipment',{}).get('multi_select',[])}
    ahead=property_text(page,'Make Ahead Notes')
    tasks=[]
    for line in lines:
        match=STEP.match(line)
        if not match: continue
        name=match.group(1).strip(); active=int(match.group(2)); waiting=int(match.group(3) or 0)
        name=re.sub(r'\s+and measure (?:sauce )?(?:ingredients|spices|milk/sugar)', '', name, flags=re.I)
        elapsed=active+waiting
        if not elapsed: continue
        number=len(tasks)+1
        fresh=any(x in name.casefold() for x in ('air-fry','fry','roast','bake','finish','assemble','sear'))
        tasks.append(PrepTask(id=f'notion-step-{number}',title=name,dependencies=[tasks[-1].id] if tasks else [],minutes=elapsed,
            active_minutes=active,presence_minutes=elapsed if active and waiting else active,unattended=active==0,resource=resource_for(name,equipment),
            scale_mode='combined' if number==1 and any(x in name.casefold() for x in ('chop','cut','rinse','mix marinade')) else 'batch',
            max_ahead_hours=None,preparation_policy='same_day',evidence='Notion home-cook timing draft (estimate)',guidance=ahead[:1500]))
    dietary=property_text(page,'Dietary Notes').casefold()
    allergens=[]
    if 'gluten: no explicit' not in dietary and 'gluten:' in dietary: allergens.append('gluten')
    if 'nuts/peanuts: no explicit' not in dietary and 'nuts/peanuts:' in dietary: allergens.append('nuts')
    # A clean ingredient screen is not an allergy clearance.
    if not allergens: allergens=None
    course=(props.get('Course',{}).get('select') or {}).get('name','Main')
    meat=re.search(r'\b(chicken|turkey|pork|beef|mutton|lamb|fish|tuna|prawn|shrimp|meat)\b',' '.join(x.name for x in ingredients),re.I)
    return RecipeSnapshot(id=page['id'],version=page.get('last_edited_time','1'),title=title,
        source=props.get('Source URL',{}).get('url') or page.get('url','notion:'+page['id']),
        servings=props.get('Base Servings',{}).get('number'),category=COURSES.get(course,'mains'),
        vegetarian=False if meat else None,allergens=allergens,ingredients=ingredients,tasks=tasks,
        source_text='\n'.join(lines)[:100000],reviewed=False,
        uncertainties=['Task timings and make-ahead limits are planning estimates; check the source and adjust before saving.',
                       'Ingredient allergy screen does not establish absence of allergens or cross-contact.'])
