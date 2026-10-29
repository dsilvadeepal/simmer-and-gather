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
