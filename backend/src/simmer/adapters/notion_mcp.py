"""App-owned scoped MCP server. Requires an explicitly configured Notion integration.
Run: uv run python -m simmer.adapters.notion_mcp
Only the three configured collections are reachable. No workspace search tool.
"""
import json, os
from mcp.server.mcpserver import MCPServer
from .notion import ScopedNotion, NotionAPITransport

server=MCPServer('Simmer and Gather recipes')
def adapter():
    return ScopedNotion(NotionAPITransport(os.environ['NOTION_TOKEN']),json.loads(os.environ['NOTION_COLLECTIONS']))

@server.tool()
def list_recipes():
    """List records only from the configured recipe collection."""
    return adapter().query('recipes')

@server.tool()
def read_recipe(page_id:str):
    """Read a recipe after verifying its collection membership."""
    return adapter().page(page_id,'recipes')

@server.tool()
def read_recipe_details(page_id:str):
    """Read a scoped recipe and its bounded top-level content blocks."""
    scoped=adapter()
    page=scoped.page(page_id,'recipes')
    blocks=[]; cursor=None
    for _ in range(10):
        path=f'/blocks/{page_id}/children?page_size=100'
        if cursor: path+='&start_cursor='+cursor
        result=scoped.transport('GET',path)
        blocks.extend(result.get('results',[]))
        if not result.get('has_more'): return {'page':page,'blocks':blocks}
        cursor=result.get('next_cursor')
        if not cursor: raise ValueError('Invalid Notion block cursor')
    raise ValueError('Recipe page exceeds 1,000 blocks')

# No write tool exposed to the planning model. Reviewed projection writes use application code.
if __name__=='__main__': server.run(transport='stdio')
