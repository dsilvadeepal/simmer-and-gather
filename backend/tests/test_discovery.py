import pytest
from simmer.discovery import RecipeDiscovery

def test_search_is_bounded_cached_and_not_a_review(store,owner):
    calls=[]
    def search(query):calls.append(query);return [{'title':'Rice','url':'https://example.com/rice','evidence_status':'unreviewed'}]
    service=RecipeDiscovery(store,search)
    a=service.search(owner,'  rice  ');b=service.search(owner,'rice')
    assert a==b and len(calls)==1
    assert len(store.list(owner,'spend'))==1
    assert store.list(owner,'recipe')==[]
    assert a[0]['evidence_status']=='unreviewed'

def test_discovery_denies_exhausted_budget_before_network(store,owner):
    from simmer.budget import Budget
    from decimal import Decimal
    Budget(store).reserve_spend(owner,'exhaust',Decimal('3'))
    with pytest.raises(ValueError):RecipeDiscovery(store,lambda q:pytest.fail('network called')).search(owner,'rice')
