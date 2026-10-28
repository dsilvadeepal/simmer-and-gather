"""Scoped Notion operations exposed to the agent; transport can be MCP backed.

No unrestricted search. Direct API transport is an explicit setup alternative,
not evidence of hosted MCP connectivity. Persist local snapshots separately.
"""
import httpx

class ScopedNotion:
    def __init__(self,transport,collections): self.transport,self.collections=transport,collections
    def scope(self,key):
        if key not in self.collections: raise ValueError('Collection outside app scope')
        return self.collections[key]
    def query(self,key):
        id=self.scope(key); cursor=None; pages=[]; seen=set()
        for _ in range(100):
            body={'page_size':100}
            if cursor: body['start_cursor']=cursor
            result=self.transport('POST',f'/data_sources/{id}/query',body)
            pages.extend(result.get('results',[]))
            if not result.get('has_more'): return pages
            cursor=result.get('next_cursor')
            if not cursor or cursor in seen: raise ValueError('Invalid pagination')
            seen.add(cursor)
        raise ValueError('Recipe collection exceeds enumeration limit')
    def page(self,id,key):
        target=self.scope(key); result=self.transport('GET',f'/pages/{id}')
        if result.get('parent',{}).get('data_source_id')!=target: raise ValueError('Page outside app scope')
        return result
    def create_reviewed(self,key,title,summary,reviewed):
        target=self.scope(key)
        if not reviewed: raise ValueError('Review required')
        return self.transport('POST','/pages',{'parent':{'type':'data_source_id','data_source_id':target},'properties':{'Name':{'title':[{'text':{'content':title[:2000]}}]}},'children':[{'object':'block','type':'paragraph','paragraph':{'rich_text':[{'type':'text','text':{'content':summary[:2000]}}]}}]})

class NotionAPITransport:
    def __init__(self,token): self.token=token
    def __call__(self,method,path,body=None):
        with httpx.Client(timeout=20) as client:
            r=client.request(method,'https://api.notion.com/v1'+path,json=body,headers={'Authorization':'Bearer '+self.token,'Notion-Version':'2025-09-03'})
            r.raise_for_status(); return r.json()
