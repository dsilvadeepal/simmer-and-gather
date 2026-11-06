import pytest
from simmer.hosting_recipe import HostingRecipeTool
from simmer.domain import RecipeSnapshot

def test_recipe_tool_reuses_results_and_preserves_review_boundary(store,owner):
    calls=[]
    def model(messages):
        calls.append(messages)
        return {'tasks':[{'id':'mix','title':'Mix batter','minutes':10,'active_minutes':10,'presence_minutes':10,'evidence':'Mix the batter','max_ahead_hours':72}]}
    recipe=RecipeSnapshot(title='Cake',source='fixture',source_text='Mix the batter')
    tool=HostingRecipeTool(store,model)
    first=tool.prepare_recipe_for_hosting(owner,recipe)
    second=tool.prepare_recipe_for_hosting(owner,recipe)
    assert len(calls)==1 and first.tasks==second.tasks
    assert not first.reviewed and first.tasks[0].max_ahead_hours is None
    recipe.source_text+=' then bake'
    tool.prepare_recipe_for_hosting(owner,recipe)
    assert len(calls)==2

def test_recipe_tool_rejects_invented_steps(store,owner):
    model=lambda _: {'tasks':[{'id':'x','title':'Freeze','minutes':5,'active_minutes':5,'presence_minutes':5,'evidence':'Freeze overnight'}]}
    with pytest.raises(ValueError,match='source evidence'):
        HostingRecipeTool(store,model).prepare_recipe_for_hosting(owner,RecipeSnapshot(title='Cake',source='fixture',source_text='Mix batter'))

def test_cache_invalidates_preferences_and_records_provenance(store,owner):
    calls=[]
    def model(messages):
        calls.append(messages)
        return {'tasks':[{'id':'mix','title':'Mix batter','minutes':10,'active_minutes':10,'presence_minutes':10,'evidence':'Mix batter'}]}
    r=RecipeSnapshot(title='Cake',source='fixture',source_text='Mix batter')
    tool=HostingRecipeTool(store,model)
    result=tool.prepare_recipe_for_hosting(owner,r,preferences={'no_measuring_tasks':True})
    tool.prepare_recipe_for_hosting(owner,r,preferences={'no_measuring_tasks':False})
    assert len(calls)==2
    assert result.preparation_provenance['schema_version']
    assert result.tasks[0].preparation_policy=='same_day'

def test_readiness_catches_missing_reheat_and_import_notes():
    from simmer.hosting_recipe import hosting_readiness
    from simmer.domain import PrepTask,Ingredient
    r=RecipeSnapshot(title='Pork',source='fixture',source_text='Cook, cool and reheat.',ingredients=[Ingredient(name='For cooking instructions, open the original source')])
    tasks=[PrepTask(id='x',title='Cook pork',minutes=60,active_minutes=15,guidance='Cook one day ahead; reheat before serving.')]
    issues=hosting_readiness(r,tasks)
    assert any('non-food' in x for x in issues)
    assert any('reheating task' in x for x in issues)
    assert any('cooling' in x for x in issues)

def test_pan_frying_cannot_be_unattended(store,owner):
    model=lambda _: {'tasks':[{'id':'x','title':'Pan-fry cutlets','minutes':25,'active_minutes':10,'presence_minutes':10,'unattended':True,'attention_segments':[{'offset_minutes':0,'minutes':5},{'offset_minutes':20,'minutes':5}],'evidence':'Fry cutlets'}]}
    r=HostingRecipeTool(store,model).prepare_recipe_for_hosting(owner,RecipeSnapshot(title='Cutlets',source='fixture',source_text='Fry cutlets'))
    assert r.tasks[0].presence_minutes==25 and not r.tasks[0].unattended

def test_invalid_checkins_rejected(store,owner):
    model=lambda _: {'tasks':[{'id':'x','title':'Bake','minutes':20,'active_minutes':5,'attention_segments':[{'offset_minutes':19,'minutes':5}],'evidence':'Bake cake'}]}
    with pytest.raises(ValueError,match='attention segments'):
        HostingRecipeTool(store,model).prepare_recipe_for_hosting(owner,RecipeSnapshot(title='Cake',source='fixture',source_text='Bake cake'))

def test_readiness_ignores_related_page_and_review_boilerplate():
    from simmer.hosting_recipe import hosting_readiness
    r=RecipeSnapshot(title='Fresh vegetables',source='fixture',source_text='{"recipeInstructions":[{"text":"Chop vegetables."}],"description":"Try overnight soaked beans and cooled cake too"}')
    assert not any('soaking' in x or 'cooling' in x for x in hosting_readiness(r,[]))

def test_dessert_leftover_reheat_is_not_a_required_task():
    from simmer.hosting_recipe import hosting_readiness
    from simmer.domain import PrepTask
    r=RecipeSnapshot(title='Cake',category='desserts',source='fixture')
    t=PrepTask(id='bake',title='Bake cake',minutes=50,active_minutes=10,presence_minutes=50,preparation_policy='same_day',guidance='Optional: reheat before serving.')
    assert not any('reheating task' in x for x in hosting_readiness(r,[t]))
