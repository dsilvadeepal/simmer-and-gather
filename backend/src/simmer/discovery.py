"""User-triggered recipe-link discovery; no automatic recipe approval/import."""
from decimal import Decimal
from hashlib import sha256
from datetime import datetime,timezone
from uuid import uuid4
from urllib.parse import urlsplit
from .budget import Budget
from .db import Missing

class RecipeDiscovery:
    def __init__(self,store,search):self.store,self.provider=store,search
    def search(self,owner,query):
        query=' '.join(query.split())
        if not query or len(query)>300:raise ValueError('Enter a recipe search of 1–300 characters')
        key=sha256((datetime.now(timezone.utc).strftime('%Y-%m-%d')+query.casefold()).encode()).hexdigest()
        try:return self.store.get(owner,'recipe_search',key)[0]['results']
        except Missing:pass
        budget=Budget(self.store);request=str(uuid4())
        if not budget.reserve_spend(owner,request,Decimal('.008')):raise ValueError('Search budget unavailable; paste a recipe link instead')
        rows=self.provider(query)
        # Basic search is one credit. Unknown/failed request keeps its reservation.
        budget.settle_spend(owner,request,Decimal('.008'))
        results=[{'title':str(x.get('title','Recipe'))[:200],'url':x['url'],'evidence_status':'unreviewed'} for x in rows if isinstance(x.get('url'),str) and urlsplit(x['url']).scheme=='https'][:3]
        from .db import Conflict
        try:self.store.put(owner,'recipe_search',key,{'results':results})
        except Conflict:pass
        return results
