import json
from pathlib import Path
from simmer.domain import PlanInputs,RecipeSnapshot
from simmer.alternatives import suggest_alternatives,trial_for
from simmer.db import Conflict
import pytest
ROOT=Path(__file__).resolve().parents[2]
CASES=json.loads((ROOT/'evals/heldout-gatherings-corrected.json').read_text())
def library():
 rows={s['recipe']['id']:RecipeSnapshot.model_validate(s['recipe']) for c in CASES for s in c['inputs']['selections'] if s.get('recipe')}
 return list(rows.values())

def test_vegetarian_alternatives_are_checked_without_mutation():
 data=PlanInputs.model_validate(CASES[17]['inputs']);before=data.model_dump(mode='json')
 result=suggest_alternatives(data,library())
 assert result['suggestions']
 for suggestion in result['suggestions']:
  assert suggestion['plan'].status=='feasible'
  assert suggestion['inputs'].gathering==data.gathering
  assert not suggestion['plan'].violations
 assert data.model_dump(mode='json')==before

def test_must_have_and_changed_recipes_cannot_be_swapped():
 data=PlanInputs.model_validate(CASES[17]['inputs']);r=library()[0]
 swap={'selection_id':data.selections[0].id,'recipe_id':r.id,'version':'stale','servings':5}
 with pytest.raises(Conflict):trial_for(data,library(),[swap])
 data.selections[0].must_have=True
 with pytest.raises(ValueError):trial_for(data,library(),[swap])

def test_unknown_allergens_never_become_cleared_by_search():
 data=PlanInputs.model_validate(CASES[15]['inputs'])
 recipes=library()
 for r in recipes:r.allergens=None
 assert not suggest_alternatives(data,recipes)['suggestions']

def test_preview_is_read_only_and_approval_rechecks_calendar(store,owner):
    from fastapi.testclient import TestClient
    from simmer.api import create_app
    from simmer.domain import AvailabilitySnapshot,Interval
    from datetime import timedelta
    class Auth:
        def require_owner(self,token):return owner
    class Calendar:
        blocked=False
        def read_availability(self,o,g,force=False):
            return AvailabilitySnapshot(status='fixture',busy=[Interval(start=g.arrival-timedelta(days=5),end=g.arrival)] if self.blocked else [])
    calendar=Calendar();data=PlanInputs.model_validate(CASES[17]['inputs'])
    store.put(owner,'gathering',data.gathering.id,data.gathering.model_dump(mode='json'))
    store.put(owner,'inputs',data.gathering.id,data.model_dump(mode='json'))
    for r in library():store.put(owner,'recipe',r.id,r.model_dump(mode='json'))
    app=create_app(store,Auth(),availability=calendar);client=TestClient(app);h={'Authorization':'Bearer test'}
    path='/api/menu/'+data.gathering.id+'/alternatives'
    store.put(owner,'plan','historical',{'test':'preserve historical plan'})
    before=store.list(owner,'inputs');plans=store.list(owner,'plan')
    response=client.post(path,headers=h,json={'expected_revision':data.gathering.revision})
    assert response.status_code==200,response.text
    option=response.json()['suggestions'][0]
    assert store.list(owner,'inputs')==before and store.list(owner,'plan')==plans
    body={'expected_revision':data.gathering.revision,'swaps':option['swaps']}
    # Changing a dish that is NOT being swapped must reject acceptance too.
    swapped={x['selection_id'] for x in option['swaps']}
    untouched=next(s.recipe for s in data.selections if s.recipe and s.id not in swapped)
    original,rev=store.get(owner,'recipe',untouched.id)
    store.put(owner,'recipe',untouched.id,{**original,'version':original['version']+'-changed'},rev)
    assert client.post(path+'/approve',headers=h,json=body).status_code==409
    assert store.list(owner,'inputs')==before and store.list(owner,'plan')==plans
    store.put(owner,'recipe',untouched.id,original,rev+1)
    calendar.blocked=True
    assert client.post(path+'/approve',headers=h,json=body).status_code==409
    assert store.list(owner,'inputs')==before
    calendar.blocked=False
    assert client.post(path+'/approve',headers=h,json=body).status_code==200
    saved_plans=store.list(owner,'plan')
    assert len(saved_plans)==len(plans)+1
    assert store.get(owner,'plan','historical')[0]=={'test':'preserve historical plan'}
    new_plan=next(p for p in saved_plans if 'plan' in p)
    assert new_plan['plan']['status']=='feasible'
    assert new_plan['plan']['revision']==data.gathering.revision+1
    from simmer.scheduler import digest
    assert new_plan['plan']['input_hash']==digest(PlanInputs.model_validate(new_plan['inputs']))
    assert client.post(path+'/approve',headers=h,json=body).status_code==409

def test_bought_option_preview_and_atomic_approval(store,owner):
    from fastapi.testclient import TestClient
    from simmer.api import create_app
    class Auth:
        def require_owner(self,token):return owner
    data=PlanInputs.model_validate(CASES[0]['inputs'])
    store.put(owner,'gathering',data.gathering.id,data.gathering.model_dump(mode='json'))
    store.put(owner,'inputs',data.gathering.id,data.model_dump(mode='json'))
    store.put(owner,'plan','keep',{'historical':True})
    client=TestClient(create_app(store,Auth(),fixture_mode=True));h={'Authorization':'Bearer test'}
    body={'expected_revision':data.gathering.revision,'selection_id':data.selections[0].id}
    path='/api/menu/'+data.gathering.id
    before=store.list(owner,'inputs')
    response=client.post(path+'/prepared-preview',headers=h,json=body)
    assert response.status_code==200,response.text
    assert response.json()['plan']['status']=='feasible'
    assert store.list(owner,'inputs')==before
    assert len(store.list(owner,'plan'))==1
    approved=client.post(path+'/prepared-approve',headers=h,json=body)
    assert approved.status_code==200,approved.text
    assert approved.json()['inputs']['selections'][0]['mode']=='buy'
    assert len(store.list(owner,'plan'))==2
    assert store.get(owner,'plan','keep')[0]=={'historical':True}
    assert client.post(path+'/prepared-approve',headers=h,json=body).status_code==409

@pytest.mark.parametrize('stage',['before_preview','after_preview'])
def test_bought_option_rejects_changed_unchanged_recipe(store,owner,stage):
    from fastapi.testclient import TestClient
    from simmer.api import create_app
    class Auth:
        def require_owner(self,token):return owner
    data=PlanInputs.model_validate(CASES[0]['inputs'])
    store.put(owner,'gathering',data.gathering.id,data.gathering.model_dump(mode='json'))
    store.put(owner,'inputs',data.gathering.id,data.model_dump(mode='json'))
    for s in data.selections:
        if s.recipe:store.put(owner,'recipe',s.recipe.id,s.recipe.model_dump(mode='json'))
    client=TestClient(create_app(store,Auth(),fixture_mode=True));h={'Authorization':'Bearer test'}
    body={'expected_revision':data.gathering.revision,'selection_id':data.selections[0].id}
    path='/api/menu/'+data.gathering.id
    if stage=='after_preview':assert client.post(path+'/prepared-preview',headers=h,json=body).status_code==200
    r=data.selections[1].recipe.model_copy(deep=True);r.version+='-changed'
    store.put(owner,'recipe',r.id,r.model_dump(mode='json'),1)
    before=store.list(owner,'inputs')
    endpoint='/prepared-preview' if stage=='before_preview' else '/prepared-approve'
    response=client.post(path+endpoint,headers=h,json=body)
    assert response.status_code==409,response.text
    assert store.list(owner,'inputs')==before and store.list(owner,'plan')==[]


def test_checked_acceptance_rechecks_recipe_after_schedule_before_commit(store,owner,monkeypatch):
    from fastapi.testclient import TestClient
    from simmer.api import create_app
    import simmer.alternatives as alternatives
    class Auth:
        def require_owner(self,token):return owner
    data=PlanInputs.model_validate(CASES[0]['inputs'])
    store.put(owner,'gathering',data.gathering.id,data.gathering.model_dump(mode='json'))
    store.put(owner,'inputs',data.gathering.id,data.model_dump(mode='json'))
    for s in data.selections:
        if s.recipe:store.put(owner,'recipe',s.recipe.id,s.recipe.model_dump(mode='json'))
    original=alternatives.checked
    def change_after_check(inputs):
        plan=original(inputs)
        recipe=data.selections[1].recipe.model_copy(deep=True);recipe.version+='-concurrent'
        store.put(owner,'recipe',recipe.id,recipe.model_dump(mode='json'),1)
        return plan
    monkeypatch.setattr(alternatives,'checked',change_after_check)
    client=TestClient(create_app(store,Auth(),fixture_mode=True))
    before=store.list(owner,'inputs');gatherings=store.list(owner,'gathering')
    response=client.post('/api/menu/'+data.gathering.id+'/prepared-approve',headers={'Authorization':'Bearer test'},json={'expected_revision':data.gathering.revision,'selection_id':data.selections[0].id})
    assert response.status_code==409
    assert store.list(owner,'inputs')==before and store.list(owner,'gathering')==gatherings
    assert not store.list(owner,'plan')
