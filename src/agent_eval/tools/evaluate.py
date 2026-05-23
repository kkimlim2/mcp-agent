# src/agent_eval/tools/evaluate.py
import os
import json
from openai import AsyncOpenAI

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