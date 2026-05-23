# tests/test_evaluate.py
import json
import pytest
from unittest.mock import AsyncMock, patch

from agent_eval.tools.evaluate import evaluate_agent_response


@pytest.mark.asyncio
async def test_evaluate_agent_response():
    mock_content = json.dumps({
        "score": 8,
        "feedback": "응답이 정확하고 간결합니다.",
        "criteria": "정확성, 간결성"
    })

    mock_message = AsyncMock()
    mock_message.choices[0].message.content = mock_content

    with patch(
        "agent_eval.tools.evaluate.client.chat.completions.create",
        new=AsyncMock(return_value=mock_message)
    ):
        result = await evaluate_agent_response(
            prompt="파이썬이란?",
            response="파이썬은 인터프리터 언어입니다.",
            criteria="정확성, 간결성"
        )

    assert result["score"] == 8
    assert "feedback" in result
    assert "criteria" in result