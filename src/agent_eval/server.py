from mcp.server.fastmcp import FastMCP
from agent_eval.tools.evaluate import evaluate_agent_response as _evaluate
from agent_eval.tools.evaluate import log_evaluation as _log
from agent_eval.tools.metrics import get_metrics_summary as _get_metrics
from agent_eval.tools.compare import compare_prompts as _compare
mcp = FastMCP("agent-eval")


@mcp.tool()
def ping() -> str:
    return "pong"


@mcp.tool()
async def evaluate_agent_response(prompt: str, response: str, criteria: str) -> dict:
    """Evaluate an agent's response using a local LLM as a judge."""
    return await _evaluate(prompt, response, criteria)

#db만 접속 -> sqlite 는 비동기 지원 x
@mcp.tool()
def log_evaluation(
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
    return _log(
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

@mcp.tool()
def compare_metrics(prompt_ids:list) -> list[dict]:
    """Compare evaluation metrics across multiple prompts."""
    return _compare(prompt_ids)

if __name__ == "__main__":
    mcp.run()