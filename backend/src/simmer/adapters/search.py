import httpx
class TavilySearch:
    def __init__(self,key,reserve): self.key,self.reserve=key,reserve
    def discover_recipes(self,query,limit=3):
        if not self.reserve(): raise ValueError('Search budget unavailable')
        with httpx.Client(timeout=20) as client:
            r=client.post('https://api.tavily.com/search',json={'api_key':self.key,'query':query[:500], 'max_results':min(max(1,limit),3),'search_depth':'basic'})
            r.raise_for_status()
            return [{'url':x['url'],'title':x['title'],'evidence_status':'unreviewed'} for x in r.json().get('results',[])][:3]
