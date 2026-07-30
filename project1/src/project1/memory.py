import sqlite3
import uuid
import time
from typing import List, Tuple

DB_PATH = "project1_memory.db"


def _connect():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = _connect()
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS sessions (
        session_id TEXT PRIMARY KEY,
        created_at REAL
    )
    """)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS messages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        session_id TEXT,
        role TEXT,
        content TEXT,
        created_at REAL
    )
    """)
    conn.commit()
    conn.close()


def create_session() -> str:
    sid = str(uuid.uuid4())
    conn = _connect()
    conn.execute("INSERT INTO sessions(session_id, created_at) VALUES(?,?)", (sid, time.time()))
    conn.commit()
    conn.close()
    return sid


def append_message(session_id: str, role: str, content: str):
    conn = _connect()
    conn.execute("INSERT INTO messages(session_id, role, content, created_at) VALUES(?,?,?,?)", (session_id, role, content, time.time()))
    conn.commit()
    conn.close()


def get_history(session_id: str, limit: int = 20) -> List[Tuple[str, str]]:
    conn = _connect()
    cur = conn.cursor()
    cur.execute("SELECT role, content FROM messages WHERE session_id=? ORDER BY id DESC LIMIT ?", (session_id, limit))
    rows = cur.fetchall()
    conn.close()
    # return most-recent-last order
    return [(r["role"], r["content"]) for r in reversed(rows)]


def prune_history(session_id: str, max_turns: int = 10):
    conn = _connect()
    cur = conn.cursor()
    # count messages
    cur.execute("SELECT COUNT(*) as c FROM messages WHERE session_id=?", (session_id,))
    total = cur.fetchone()[0]
    if total <= max_turns:
        conn.close()
        return
    # delete oldest
    to_delete = total - max_turns
    cur.execute("DELETE FROM messages WHERE id IN (SELECT id FROM messages WHERE session_id=? ORDER BY id ASC LIMIT ?)", (session_id, to_delete))
    conn.commit()
    conn.close()
