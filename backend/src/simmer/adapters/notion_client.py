"""Application MCP client; scoped read tools only, no model-controlled writes."""
import asyncio,json,os,sys
from mcp import ClientSession,StdioServerParameters
from mcp.client.stdio import stdio_client
from ..domain import RecipeSnapshot

class NotionRecipes:
    def __init__(self,token,collections): self.token,self.collections=token,collections
    async def _list(self):
        env={k:v for k,v in os.environ.items() if k in ('PATH','SYSTEMROOT','HOME')}
        env.update(NOTION_TOKEN=self.token,NOTION_COLLECTIONS=json.dumps(self.collections))
        params=StdioServerParameters(command=sys.executable,args=['-m','simmer.adapters.notion_mcp'],env=env)
        async with stdio_client(params) as (read,write):
            async with ClientSession(read,write) as session:
                await session.initialize()
                result=await session.call_tool('list_recipes',{},read_timeout_seconds=20)
                if result.is_error: raise ValueError('Notion recipe lookup failed')
                rows=[]
                for block in result.content:
                    if getattr(block,'type',None)=='text':
                        data=json.loads(block.text)
                        rows.extend(data if isinstance(data,list) else [data])
                return rows
    def list_candidates(self):
        async def bounded(): return await asyncio.wait_for(self._list(),timeout=25)
        return [candidate_from_page(page) for page in asyncio.run(bounded())]

def candidate_from_page(page):
    props=page.get('properties',{})
    title=''.join(x.get('plain_text',x.get('text',{}).get('content','')) for p in props.values() if p.get('type')=='title' for x in p.get('title',[]))
    source=props.get('Source URL',{}).get('url') or page.get('url','notion:'+page['id'])
    return RecipeSnapshot(id=page['id'],version=page.get('last_edited_time','1'),title=title or 'Notion recipe',source=source,
                          servings=props.get('Base Servings',{}).get('number'),reviewed=False,
                          uncertainties=['Import source and review task timings and storage before planning'])
