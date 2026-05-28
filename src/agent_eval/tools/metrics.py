from agent_eval.db_hook import get_conn


def get_metrics_summary(agent_id: str, prompt_id: str, conn=None) -> dict:
    _conn = conn or get_conn()
    row = _conn.execute(
        """
        SELECT
            COUNT(*)           AS total_count,
            AVG(overall_score) AS avg_score,
            AVG(passed)        AS pass_rate
        FROM evaluations
        WHERE agent_id  = :agent_id
          AND prompt_id = :prompt_id
        """,
        {"agent_id": agent_id, "prompt_id": prompt_id},
    ).fetchone()

    return {
        "agent_id": agent_id,
        "prompt_id": prompt_id,
        "total_count": row["total_count"] or 0,
        "avg_score": round(row["avg_score"], 4) if row["avg_score"] else None,
        "pass_rate": round(row["pass_rate"], 4) if row["pass_rate"] else None,
    }