from simmer.adapters.notion_client import candidate_from_page
from simmer.adapters.notion_recipe_details import from_notion_details, ingredient

def test_notion_planning_ready_never_bypasses_app_review():
    page={'id':'r','last_edited_time':'v2','properties':{'Recipe':{'type':'title','title':[{'plain_text':'Rice'}]},'Planning Ready':{'checkbox':True},'Source URL':{'url':'https://example.com/rice'},'Base Servings':{'number':4}}}
    r=candidate_from_page(page)
    assert r.title=='Rice' and r.servings==4
    assert r.reviewed is False and not r.tasks and r.uncertainties

def test_notion_details_make_editable_draft_with_estimated_tasks():
    page={'id':'recipe-1','last_edited_time':'v3','properties':{
        'Recipe':{'title':[{'plain_text':'Paneer Tikka'}]},
        'Source URL':{'url':'https://example.com/paneer'},
        'Base Servings':{'number':8},
        'Course':{'select':{'name':'Starter'}},
        'Equipment':{'multi_select':[{'name':'Air fryer'},{'name':'Refrigerator'}]},
        'Make Ahead Notes':{'rich_text':[{'plain_text':'Marinate the night before.'}]},
        'Dietary Notes':{'rich_text':[{'plain_text':'Gluten: No explicit listed ingredient matched. Nuts/peanuts: No explicit listed ingredient matched.'}]},
    }}
    def block(text,kind='paragraph'):
        return {'type':kind,kind:{'rich_text':[{'plain_text':text}]}}
    blocks=[block('Ingredients (source facts; quantities need confirmation before scaling)'),
            block('½ cup yogurt'),block('1 ½ teaspoons salt'),block('Cooking method and recipe notes: open the original source link.'),
            block('Home-cook timing draft (untested)','heading_3'),
            block('Marinate in refrigerator: 0 min hands-on + 30 min waiting/cooking','bulleted_list_item'),
            block('Skewer and air-fry one batch: 10 min hands-on + 10 min waiting/cooking','bulleted_list_item')]
    r=from_notion_details(page,blocks)
    assert r.title=='Paneer Tikka' and r.servings==8 and r.category=='starters'
    assert r.reviewed is False and r.allergens is None
    assert len(r.ingredients)==2 and r.ingredients[0].quantity==.5
    assert len(r.tasks)==2 and r.tasks[1].resource=='air_fryer'
    assert r.tasks[1].dependencies==[r.tasks[0].id]
    assert r.tasks[0].minutes==30 and r.tasks[0].active_minutes==0

def test_ingredient_parser_keeps_unrecognized_quantities_visible():
    assert ingredient('1/2 cup yogurt').quantity==.5
    assert ingredient('1 1/2 cups rice').quantity==1.5
    assert ingredient('a handful of mint').name=='a handful of mint'

def test_import_reserves_return_attention_after_waiting():
    from simmer.domain import Assignment,Interval
    from simmer.scheduler import occupancy_windows
    page={'id':'r','properties':{'Recipe':{'title':[{'plain_text':'Roast'}]}}}
    blocks=[{'type':'paragraph','paragraph':{'rich_text':[{'plain_text':'Roast and briefly broil; check doneness: 10 min hands-on + 40 min waiting/cooking'}]}}]
    t=from_notion_details(page,blocks).tasks[0]
    a=Assignment(task=t,interval=Interval(start='2026-11-01T17:00:00-05:00',end='2026-11-01T17:50:00-05:00'))
    assert any(w.end==a.interval.end for w in occupancy_windows(a,[],True))

def test_changed_unparsed_notion_method_never_restores_seed():
    page={'id':'r','properties':{'Recipe':{'title':[{'plain_text':'Paneer'}]},'Source URL':{'url':'https://ministryofcurry.com/paneer-tikka/'}}}
    blocks=[{'type':'paragraph','paragraph':{'rich_text':[{'plain_text':'Saute paneer on stovetop instead of air-frying; omit skewers.'}]}}]
    assert from_notion_details(page,blocks).tasks==[]
