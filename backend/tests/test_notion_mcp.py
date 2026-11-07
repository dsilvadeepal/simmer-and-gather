def test_scoped_mcp_server_imports_with_pinned_sdk():
    from simmer.adapters.notion_mcp import server
    assert server is not None
