"""Scoped Notion operations exposed to the agent; transport can be MCP backed.

No unrestricted search. Direct API transport is an explicit setup alternative,
not evidence of hosted MCP connectivity. Persist local snapshots separately.
"""
import httpx

class BeforeWriteError(ValueError): pass

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
        schema=self.transport('GET',f'/data_sources/{target}')
        titles=[name for name,prop in schema.get('properties',{}).items() if prop.get('type')=='title']
        if len(titles)!=1: raise ValueError('Expected one title property in approved collection')
        return self.transport('POST','/pages',{'parent':{'type':'data_source_id','data_source_id':target},'properties':{titles[0]:{'title':[{'text':{'content':title[:2000]}}]}},'children':[{'object':'block','type':'paragraph','paragraph':{'rich_text':[{'type':'text','text':{'content':summary[:2000]}}]}}]})

    def title_property(self,key):
        schema=self.transport('GET',f'/data_sources/{self.scope(key)}')
        titles=[name for name,prop in schema.get('properties',{}).items() if prop.get('type')=='title']
        if len(titles)!=1: raise ValueError('Expected one title property')
        return titles[0]
    def find_projection(self,key,title):
        prop=self.title_property(key)
        result=self.transport('POST',f'/data_sources/{self.scope(key)}/query',{'filter':{'property':prop,'title':{'equals':title}},'page_size':100})
        if result.get('has_more'): raise ValueError('Ambiguous projection')
        return result.get('results',[])
    def create_projection(self,key,title,lines,properties=None):
        try:
            chunks=[line[i:i+1800] for line in lines for i in range(0,len(line),1800)]
            if len(chunks)>100: raise ValueError('Recipe or plan exceeds single-page export limit')
            payload={'parent':{'type':'data_source_id','data_source_id':self.scope(key)},'properties':{**(properties or {}),self.title_property(key):{'title':[{'text':{'content':title}}]}},'children':[{'object':'block','type':'paragraph','paragraph':{'rich_text':[{'type':'text','text':{'content':line}}]}} for line in chunks]}
        except Exception as e: raise BeforeWriteError('Notion export could not be prepared') from e
        try: return self.transport('POST','/pages',payload)
        except httpx.HTTPStatusError as e:
            if e.response.status_code in (400,401,403,404,413,422,429): raise BeforeWriteError('Notion rejected the write') from e
            raise

class NotionAPITransport:
    def __init__(self,token): self.token=token
    def __call__(self,method,path,body=None):
        with httpx.Client(timeout=20) as client:
            r=client.request(method,'https://api.notion.com/v1'+path,json=body,headers={'Authorization':'Bearer '+self.token,'Notion-Version':'2025-09-03'})
            r.raise_for_status(); return r.json()
