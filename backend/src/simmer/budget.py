from datetime import datetime,timezone
from decimal import Decimal
from .db import Missing,serialized

class Budget:
    def __init__(self,store,ceiling=Decimal('3')):
        self.store=store;self.ceiling=ceiling
        if not ceiling.is_finite() or not 0<=ceiling<=3: raise ValueError('AI budget must leave $2 of the $5 total envelope')
    @serialized
    def reserve_spend(self,owner,request_id,estimated_usd):
        estimate=Decimal(str(estimated_usd))
        if not estimate.is_finite() or estimate<0: return False
        try: self.store.get(owner,'spend',request_id);return False
        except Missing: pass
        month=datetime.now(timezone.utc).strftime('%Y-%m')
        spent=sum(Decimal(x['charged']) for x in self.store.list(owner,'spend') if x['month']==month)
        if spent+estimate>self.ceiling: return False
        self.store.put(owner,'spend',request_id,{'month':month,'reserved':str(estimate),'charged':str(estimate),'settled':False})
        return True
    @serialized
    def settle_spend(self,owner,request_id,actual_usd):
        value,rev=self.store.get(owner,'spend',request_id)
        if actual_usd is None or value['settled']: return
        actual=Decimal(str(actual_usd))
        if not actual.is_finite() or actual<0: raise ValueError('Invalid usage cost')
        self.store.put(owner,'spend',request_id,{**value,'charged':str(actual),'settled':True},rev)
