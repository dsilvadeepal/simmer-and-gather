import pytest
from pydantic import ValidationError
from simmer.domain import Ingredient, QuantityDetail
from simmer.quantities import scale_amount
from simmer.scheduler import schedule
from test_scheduler import inputs

def test_quantity_range_preserves_source_and_scales_without_mutation():
    row=Ingredient(name='sugar',unit='cup',amount_detail=QuantityDetail(kind='range',minimum=1,maximum=2,source_text='1–2 cups sugar',basis='source'))
    scaled=scale_amount(row,3)
    assert scaled.quantity is None
    assert (scaled.amount_detail.minimum,scaled.amount_detail.maximum)==(3,6)
    assert row.amount_detail.minimum==1
    assert scaled.amount_detail.source_text=='1–2 cups sugar'

def test_legacy_and_unknown_amounts():
    assert scale_amount(Ingredient(name='salt to taste'),3).amount_detail.kind=='to_taste'
    assert scale_amount(Ingredient(name='onion',quantity=2),3).quantity==6
    assert scale_amount(Ingredient(name='onion',quantity=2),None).amount_detail.kind=='unknown'
    with pytest.raises(ValidationError):
        QuantityDetail(kind='range',minimum=3,maximum=2)

def test_scheduler_explains_missing_inputs():
    data=inputs()
    data.selections[0].recipe.tasks[0].minutes=None
    assert schedule(data).outcome.code=='needs_input'

@pytest.mark.parametrize('solver_status,code',[('UNKNOWN','search_exhausted'),('UNSUPPORTED','unsupported'),('INFEASIBLE','no_fit_found')])
def test_solver_failure_is_not_reported_as_proven_time_shortage(monkeypatch,solver_status,code):
    def fail(data,diagnostics):
        diagnostics['solver_status']=solver_status
    monkeypatch.setattr('simmer.constraint_scheduler.solve_schedule',fail)
    plan=schedule(inputs())
    assert plan.outcome.code==code
    assert plan.status!='feasible'

def test_feasible_plan_has_complete_outcome():
    assert schedule(inputs(limit=90)).outcome.code=='complete'

def test_range_import_and_shopping_flow():
    from simmer.adapters.notion_recipe_details import ingredient
    from simmer.inventory import shopping_for
    data=inputs()
    data.selections[0].recipe.ingredients=[ingredient('1 to 2 cups sugar')]
    data.selections[0].servings=30
    row=shopping_for(data)[0]
    assert row.name=='sugar'
    assert row.quantity is None
    assert (row.amount_detail.minimum,row.amount_detail.maximum)==(2,4)

def test_broken_dependency_is_input_problem_not_time_problem():
    data=inputs()
    data.selections[0].recipe.tasks[0].dependencies=['missing']
    plan=schedule(data)
    assert plan.outcome.code=='needs_input'
    assert any(v.code=='recipe_contract' for v in plan.violations)

def test_dependency_cycle_is_rejected():
    from simmer.recipe_contracts import task_contract_errors
    data=inputs()
    tasks=data.selections[0].recipe.tasks
    tasks[0].dependencies=[tasks[1].id]
    tasks[1].dependencies=[tasks[0].id]
    assert any('cycle' in x for x in task_contract_errors(tasks))

def test_old_hash_unchanged_with_absent_additive_fields():
    from simmer.scheduler import digest
    import hashlib,json
    old={'name':'onion','quantity':2.0,'unit':'count'}
    expected=hashlib.sha256(json.dumps(old,sort_keys=True,separators=(',',':')).encode()).hexdigest()
    assert digest(Ingredient.model_validate(old))==expected

def test_api_full_flow_preserves_quantity_contract_and_outcome(store,owner):
    from fastapi.testclient import TestClient
    from simmer.api import create_app
    from simmer.adapters.notion_recipe_details import ingredient
    class Auth:
        def require_owner(self,token): return owner
    client=TestClient(create_app(store,Auth(),fixture_mode=True))
    headers={'Authorization':'Bearer isolated-test'}
    data=inputs(minutes=(20,),limit=90)
    data.selections[0].recipe.ingredients=[ingredient('1 to 2 cups sugar')]
    result=client.post('/api/gatherings',headers=headers,json={'gathering':data.gathering.model_dump(mode='json')})
    assert result.status_code==200
    gathering=result.json()
    edited=client.post('/api/menu/'+gathering['id'],headers=headers,json={'expected_revision':gathering['revision'],'changes':[{'action':'add','selection':data.selections[0].model_dump(mode='json')}]})
    assert edited.status_code==200
    revision=edited.json()['gathering']['revision']
    generated=client.post('/api/plans/'+gathering['id']+'/generate',headers=headers,json={'expected_revision':revision})
    assert generated.status_code==200
    plan=generated.json()
    assert plan['outcome']['code']=='complete'
    assert plan['shopping'][0]['amount_detail']['kind']=='range'
    workspace=client.get('/api/workspace/'+gathering['id'],headers=headers).json()
    assert workspace['plan']['outcome']==plan['outcome']
    # No booking endpoints or external integrations are invoked in this fixture flow.

def test_menu_unknowns_override_complete_schedule():
    from simmer.agent import apply_menu_validation
    data=inputs(minutes=(20,),limit=90)
    plan=schedule(data)
    assert plan.outcome.code=='complete'
    data.gathering.allergies=['nuts']
    plan=apply_menu_validation(data,plan)
    assert plan.status=='incomplete'
    assert plan.outcome.code=='needs_input'


def test_menu_review_does_not_erase_schedule_failure():
    from simmer.agent import apply_menu_validation
    from simmer.domain import PlanCandidate, SchedulingOutcome
    data=inputs()
    data.gathering.allergies=['nuts']
    plan=PlanCandidate(gathering_id=data.gathering.id,revision=1,input_hash='test',status='conflict',outcome=SchedulingOutcome(code='no_fit_found',message='No available time',solver_status='INFEASIBLE'))
    result=apply_menu_validation(data,plan)
    assert result.outcome.code=='no_fit_found'
    assert result.outcome.solver_status=='INFEASIBLE'
    assert any(v.code=='allergy_unknown' for v in result.violations)


def test_notion_structured_recipe_preserves_timing_but_requires_review():
    import json
    from simmer.adapters.notion_recipe_details import from_notion_details
    r=inputs(minutes=(20,),limit=90).selections[0].recipe
    page={'id':'notion-page','last_edited_time':'today','properties':{'Source URL':{'url':r.source}}}
    data={'type':'code','code':{'caption':[{'text':{'content':'Simmer and Gather recipe data v1'}}],'rich_text':[{'text':{'content':r.model_dump_json()}}]}}
    back=from_notion_details(page,[data])
    assert back.tasks==r.tasks
    assert back.reviewed is False
    assert back.id=='notion-page'
