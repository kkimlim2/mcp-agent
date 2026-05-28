import sqlite3
import pytest
from agent_eval.tools.compare import compare_prompts


@pytest.fixture
def conn():
    conn = sqlite3.connect(":memory:")
    conn.executescript("""
        CREATE TABLE prompts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        CREATE TABLE evaluations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            prompt_id INTEGER REFERENCES prompts(id),
            score INTEGER,
            criteria TEXT,
            reasoning TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)
    conn.execute("INSERT INTO prompts (content) VALUES ('프롬프트 A 내용')")
    conn.execute("INSERT INTO prompts (content) VALUES ('프롬프트 B 내용')")
    conn.executemany(
        "INSERT INTO evaluations (prompt_id, score, criteria, reasoning) VALUES (?,?,?,?)",
        [
            (1, 8, "accuracy", "good"),
            (1, 6, "accuracy", "ok"),
            (2, 9, "accuracy", "great"),
            (2, 10, "accuracy", "perfect"),
        ]
    )
    conn.commit()
    yield conn
    conn.close()


def test_compare_returns_both_prompts(conn):
    result = compare_prompts([1, 2], conn=conn)
    assert len(result) == 2


def test_compare_ordered_by_avg_score(conn):
    result = compare_prompts([1, 2], conn=conn)
    # prompt 2 평균(9.5) > prompt 1 평균(7.0)
    assert result[0]["prompt_id"] == 2
    assert result[1]["prompt_id"] == 1


def test_compare_avg_score_correct(conn):
    result = compare_prompts([1, 2], conn=conn)
    scores = {r["prompt_id"]: r["avg_score"] for r in result}
    assert scores[1] == 7.0
    assert scores[2] == 9.5


def test_compare_empty_input(conn):
    result = compare_prompts([], conn=conn)
    assert result == []


def test_compare_prompt_with_no_evaluations(conn):
    conn.execute("INSERT INTO prompts (content) VALUES ('평가 없는 프롬프트')")
    conn.commit()
    result = compare_prompts([3], conn=conn)
    assert result[0]["eval_count"] == 0
    assert result[0]["avg_score"] is None


def test_content_not_truncated(conn):
    long_content = "A" * 200
    conn.execute(f"INSERT INTO prompts (content) VALUES ('{long_content}')")
    conn.commit()
    result = compare_prompts([3], conn=conn)
    assert len(result[0]["prompt_content"]) == 200