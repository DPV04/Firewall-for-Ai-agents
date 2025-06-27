# initialize_db.py
import sqlite3
from .config import DB_PATH

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT,
            query_text TEXT,
            blocked INTEGER,
            reason TEXT,
            matches TEXT,
            tactic TEXT,
            technique_id TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()
    print(f"✅ Initialized database at {DB_PATH}")

if __name__ == "__main__":
    init_db()
