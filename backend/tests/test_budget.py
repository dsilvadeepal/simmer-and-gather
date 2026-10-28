from decimal import Decimal
from concurrent.futures import ThreadPoolExecutor
from simmer.budget import Budget

def test_simultaneous_reservations_cannot_overdraw(store,owner):
    budget=Budget(store,ceiling=Decimal('3'))
    with ThreadPoolExecutor(2) as pool:
        results=list(pool.map(lambda id:budget.reserve_spend(owner,id,Decimal('2')),['a','b']))
    assert sum(results)==1

def test_duplicate_calls_and_unknown_cost_keep_reservation(store,owner):
    b=Budget(store,ceiling=Decimal('0.5'))
    assert b.reserve_spend(owner,'a',Decimal('.4'))
    assert not b.reserve_spend(owner,'a',Decimal('.4'))
    b.settle_spend(owner,'a',None)
    assert not b.reserve_spend(owner,'b',Decimal('.2'))
    b.settle_spend(owner,'a',Decimal('.1'))
    assert b.reserve_spend(owner,'b',Decimal('.2'))
