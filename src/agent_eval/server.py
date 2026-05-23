# src/agent_eval/server.py
from mcp.server.fastmcp import FastMCP
from agent_eval.tools.evaluate import evaluate_agent_response as _evaluate

mcp = FastMCP("agent-eval")

@mcp.tool()
def ping() -> str:
    return "pong"

@mcp.tool()
async def evaluate_agent_response(prompt: str, response: str, criteria: str) -> dict:
    """Evaluate an agent's response using a local LLM as a judge."""
    return await _evaluate(prompt, response, criteria)

if __name__ == "__main__":
    mcp.run()