import pytest
from simmer.runtime import build_text_model
from simmer.db import Missing

def test_runtime_paid_calls_disabled_without_explicit_switch(store,owner):
    assert build_text_model(store,owner,{'FIREWORKS_API_KEY':'test'}) is None

def test_runtime_denies_unknown_model_and_missing_key(store,owner):
    with pytest.raises(ValueError): build_text_model(store,owner,{'ENABLE_PAID_MODELS':'true','PLANNING_MODEL':'unknown','FIREWORKS_API_KEY':'test'})
    with pytest.raises(ValueError): build_text_model(store,owner,{'ENABLE_PAID_MODELS':'true'})

def test_runtime_reserves_and_settles_actual_usage(store,owner,monkeypatch):
    import simmer.runtime as runtime
    class FakeClient:
        def __init__(self,url,key,model,reserve,settle): self.reserve,self.settle=reserve,settle
        def complete(self,messages,request_id,max_tokens):
            assert self.reserve(request_id)
            self.settle(request_id,{'prompt_tokens':1000,'completion_tokens':100})
            return '{"recipe_ids":[]}'
    monkeypatch.setattr(runtime,'ModelClient',FakeClient)
    model=build_text_model(store,owner,{'ENABLE_PAID_MODELS':'true','FIREWORKS_API_KEY':'test'})
    assert model([{'role':'user','content':'hello'}])=='{"recipe_ids":[]}'
    rows=store.list(owner,'spend'); assert len(rows)==1
    assert float(rows[0]['charged'])==pytest.approx(.0002)
    with pytest.raises(ValueError): model([{'role':'user','content':[{'type':'image_url'}]}])
    assert len(store.list(owner,'spend'))==1
