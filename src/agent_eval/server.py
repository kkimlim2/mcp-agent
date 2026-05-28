from mcp.server.fastmcp import FastMCP
from agent_eval.tools.evaluate import evaluate_agent_response as _evaluate
from agent_eval.tools.evaluate import log_evaluation as _log
from agent_eval.tools.metrics import get_metrics_summary as _get_metrics

mcp = FastMCP("agent-eval")


@mcp.tool()
def ping() -> str:
    return "pong"


@mcp.tool()
async def evaluate_agent_response(prompt: str, response: str, criteria: str) -> dict:
    """Evaluate an agent's response using a local LLM as a judge."""
    return await _evaluate(prompt, response, criteria)


@mcp.tool()
async def log_evaluation(
    agent_id: str,
    prompt_id: str,
    query: str,
    response: str,
    overall_score: float,
    passed: bool,
    scores: dict | None = None,
    metadata: dict | None = None,
    tags: list | None = None,
) -> dict:
    """Log an evaluation result to the database."""
    return await _log(
        agent_id=agent_id,
        prompt_id=prompt_id,
        query=query,
        response=response,
        overall_score=overall_score,
        passed=passed,
        scores=scores,
        metadata=metadata,
        tags=tags,
    )


@mcp.tool()
def get_metrics_summary(agent_id: str, prompt_id: str) -> dict:
    """Get aggregated evaluation metrics for a specific agent and prompt."""
    return _get_metrics(agent_id=agent_id, prompt_id=prompt_id)


if __name__ == "__main__":
    mcp.run()