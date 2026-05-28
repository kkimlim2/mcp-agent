import sqlite3
from agent_eval.db_hook import get_conn


def compare_prompts(prompt_ids: list[int], conn: sqlite3.Connection | None = None) -> list[dict]:
    """
    여러 프롬프트의 평가 지표를 비교합니다.

    Args:
        prompt_ids: 비교할 prompt id 리스트
        conn: DB 커넥션 (테스트용 의존성 주입)
    """
    if not prompt_ids:
        return []

    should_close = conn is None
    if conn is None:
        conn = get_connection()

    try:
        placeholders = ",".join("?" * len(prompt_ids))
        query = f"""
            SELECT
                p.id            AS prompt_id,
                p.content       AS prompt_content,
                COUNT(e.id)     AS eval_count,
                ROUND(AVG(e.score), 2) AS avg_score,
                MAX(e.score)    AS max_score,
                MIN(e.score)    AS min_score
            FROM prompts p
            LEFT JOIN evaluations e ON e.prompt_id = p.id
            WHERE p.id IN ({placeholders})
            GROUP BY p.id
            ORDER BY avg_score DESC
        """
        cursor = conn.execute(query, prompt_ids)
        rows = cursor.fetchall()

        return [
            {
                "prompt_id": row[0],
                "prompt_content": row[1],
                "eval_count": row[2],
                "avg_score": row[3],
                "max_score": row[4],
                "min_score": row[5],
            }
            for row in rows
        ]
    finally:
        if should_close:
            conn.close()