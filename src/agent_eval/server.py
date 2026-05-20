from mcp.server.fastmcp import FastMCP

mcp = FastMCP("agent-eval")

@mcp.tool()
def ping() -> str:
    """서버 상태 확인"""
    return "agent-eval MCP server is running"

if __name__ == "__main__":
    mcp.run()