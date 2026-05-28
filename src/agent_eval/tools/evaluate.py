# src/agent_eval/tools/evaluate.py
import os
import json
import uuid
from openai import AsyncOpenAI
from agent_eval.db_hook import get_conn

client = AsyncOpenAI(
    base_url=os.getenv("LLM_BASE_URL", "http://localhost:11434/v1"),
    api_key="ollama",
)
MODEL = os.getenv("LLM_MODEL", "llama3")


async def evaluate_agent_response(prompt: str, response: str, criteria: str) -> dict:
    result = await client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are an expert AI response evaluator. "
                    "Score the given response from 1 to 10 based on the provided criteria. "
                    "Return ONLY a JSON object with keys: score (int), feedback (str), criteria (str). "
                    "No explanation outside the JSON."
                ),
            },
            {
                "role": "user",
                "content": (
                    f"Prompt: {prompt}\n\n"
                    f"Response: {response}\n\n"
                    f"Criteria: {criteria}"
                ),
            },
        ],
    )
    raw = result.choices[0].message.content
    return json.loads(raw)


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
    conn=None,
) -> dict:
    record_id = str(uuid.uuid4())

    _conn = conn or get_conn()
    with _conn:
        _conn.execute(
            """
            INSERT INTO evaluations
                (id, agent_id, prompt_id, query, response,
                 scores, overall_score, passed, metadata, tags)
            VALUES
                (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                record_id,
                agent_id,
                prompt_id,
                query,
                response,
                json.dumps(scores) if scores else None,
                overall_score,
                int(passed),
                json.dumps(metadata) if metadata else None,
                json.dumps(tags) if tags else None,
            ),
        )

    return {"id": record_id}