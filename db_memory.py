import sqlite3
from pathlib import Path
from typing import List, Tuple

# Path to the SQLite DB (placed next to this file)
DB_PATH = Path(__file__).with_name("chat_log.db")

def _conn():
    """Create a new SQLite connection (thread‑safe)."""
    return sqlite3.connect(DB_PATH, check_same_thread=False)

def init_db() -> None:
    """Create tables if they don't exist yet."""
    conn = _conn()
    cur = conn.cursor()
    cur.execute(
        """CREATE TABLE IF NOT EXISTS messages (
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               role TEXT NOT NULL,
               content TEXT NOT NULL,
               ts DATETIME DEFAULT CURRENT_TIMESTAMP
           );"""
    )
    cur.execute(
        """CREATE TABLE IF NOT EXISTS deadlines (
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               date TEXT NOT NULL,      -- DD‑MM‑YYYY
               description TEXT NOT NULL,
               ts DATETIME DEFAULT CURRENT_TIMESTAMP
           );"""
    )
    conn.commit()
    conn.close()

def save_message(role: str, content: str) -> None:
    """Persist a single chat turn."""
    conn = _conn()
    conn.execute("INSERT INTO messages (role, content) VALUES (?, ?)", (role, content))
    conn.commit()
    conn.close()

def get_last_messages(limit: int = 10) -> List[Tuple[str, str, str]]:
    """Return the most recent `limit` messages as (role, content, timestamp).
    Timestamp is stored as SQLite default string (ISO‑8601)."""
    conn = _conn()
    cur = conn.cursor()
    cur.execute(
        "SELECT role, content, ts FROM messages ORDER BY id DESC LIMIT ?",
        (limit,)
    )
    rows = cur.fetchall()
    conn.close()
    # Normalize rows: older tables may lack the ts column, yielding 2‑element tuples.
    normalized: List[Tuple[str, str, str]] = []
    for row in rows:
        if len(row) == 2:
            role, content = row
            ts = ""
        else:
            role, content, ts = row
        normalized.append((role, content, ts))
    return normalized[::-1]

def add_deadline(date_str: str, description: str) -> None:
    """Store a deadline in the DB. `date_str` must be DD‑MM‑YYYY as per user convention."""
    conn = _conn()
    conn.execute(
        "INSERT INTO deadlines (date, description) VALUES (?, ?)", (date_str, description)
    )
    conn.commit()
    conn.close()

def get_all_deadlines() -> List[Tuple[str, str]]:
    """Return all stored deadlines (date, description) ordered by insertion."""
    conn = _conn()
    cur = conn.cursor()
    cur.execute("SELECT date, description FROM deadlines ORDER BY id ASC")
    rows = cur.fetchall()
    conn.close()
    return rows
