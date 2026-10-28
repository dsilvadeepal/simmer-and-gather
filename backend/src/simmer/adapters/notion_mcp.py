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

# No write tool exposed to the planning model. Reviewed projection writes use application code.
if __name__=='__main__': server.run(transport='stdio')
