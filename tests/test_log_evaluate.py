# tests/test_log_evaluation.py
import sqlite3
import pytest
from pathlib import Path
from agent_eval.tools.evaluate import log_evaluation

DDL_PATH = Path(__file__).parent.parent / "sql" / "ddl.sql"


@pytest.fixture
def memory_db():
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row
    conn.executescript(DDL_PATH.read_text())
    return conn


def test_log_evaluation_saves_to_db(memory_db):
    result = log_evaluation(
        agent_id="test-agent",
        prompt_id="prompt-001",
        query="환불 방법이 뭐야?",
        response="고객센터에 문의하세요.",
        overall_score=7.5,
        passed=True,
        conn=memory_db,
    )

    assert "id" in result

    row = memory_db.execute(
        "SELECT * FROM evaluations WHERE id = ?", (result["id"],)
    ).fetchone()

    assert row is not None
    assert row["agent_id"] == "test-agent"
    assert row["overall_score"] == 7.5
    assert row["passed"] == 1