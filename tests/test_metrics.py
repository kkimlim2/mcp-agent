import sqlite3
import pytest
from agent_eval.tools.metrics import get_metrics_summary


@pytest.fixture
def conn():
    c = sqlite3.connect(":memory:")
    c.row_factory = sqlite3.Row
    c.executescript(open("sql/ddl.sql").read())
    yield c #pytest fixture: yield 앞은 setup, yield 값은 테스트 함수에 자동 주입
    c.close()


def test_get_metrics_summary(conn):
    # Given
    conn.execute(
        "INSERT INTO prompts (id, agent_id, version, content) VALUES (?,?,?,?)",
        ("p1", "bot-a", "v1", "prompt content"),
    )
    conn.executemany(
        """INSERT INTO evaluations
           (id, agent_id, prompt_id, overall_score, passed)
           VALUES (?,?,?,?,?)""",
        [
            ("e1", "bot-a", "p1", 0.9, 1),
            ("e2", "bot-a", "p1", 0.7, 1),
            ("e3", "bot-a", "p1", 0.5, 0),
        ],
    )
    conn.commit()

    # When
    result = get_metrics_summary(agent_id="bot-a", prompt_id="p1", conn=conn)

    # Then
    assert result["total_count"] == 3
    assert result["avg_score"] == round((0.9 + 0.7 + 0.5) / 3, 4)
    assert result["pass_rate"] == round(2 / 3, 4)


def test_get_metrics_summary_empty(conn):
    # 평가 데이터 없을 때
    conn.execute(
        "INSERT INTO prompts (id, agent_id, version, content) VALUES (?,?,?,?)",
        ("p1", "bot-a", "v1", "prompt content"),
    )
    conn.commit()

    result = get_metrics_summary(agent_id="bot-a", prompt_id="p1", conn=conn)

    assert result["total_count"] == 0
    assert result["avg_score"] is None
    assert result["pass_rate"] is None