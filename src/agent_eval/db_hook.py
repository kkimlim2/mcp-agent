import sqlite3
import os
from pathlib import Path

DB_PATH = os.environ.get("DB_PATH", "agent_eval.db")
DDL_PATH = Path(__file__).parent / "sql" / "ddl.sql"


def get_conn() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    ddl = DDL_PATH.read_text()
    with get_conn() as conn:
        conn.executescript(ddl)