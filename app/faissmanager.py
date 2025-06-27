import faiss
import os
import numpy as np
import sqlite3
from .config import DB_PATH, DOMAIN_INDEXES

def ensure_sqlite_db():
    with sqlite3.connect(DB_PATH) as conn:
        # Table for embedding metadata (existing)
        conn.execute("""
    CREATE TABLE IF NOT EXISTS metadata (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        domain TEXT,
        vector_index INTEGER,
        source TEXT,
        text TEXT,  
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    );
     """)

        
       
        conn.execute("""
            CREATE TABLE IF NOT EXISTS query_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT,
                domain TEXT,
                query TEXT,
                blocked BOOLEAN,
                reason TEXT,
                matches TEXT,
                tactic TEXT,
                technique_id TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            );
        """)
        conn.commit()

def load_index(domain: str):
    ensure_sqlite_db()
    index_path = DOMAIN_INDEXES[domain]["index"]
    if not os.path.exists(index_path):
        return faiss.IndexFlatL2(384), []

    index = faiss.read_index(index_path)

    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.execute(
            "SELECT source, text FROM metadata WHERE domain = ? ORDER BY vector_index",
            (domain,)
        )
        meta = [
    f"{row[0]}: {row[1][:100]}..." if row[1] else f"{row[0]}: [no preview]"
    for row in cursor.fetchall()
]
    return index, meta

def save_index(domain: str, index, metadata_list):
    ensure_sqlite_db()
    index_path = DOMAIN_INDEXES[domain]["index"]
    faiss.write_index(index, index_path)

    with sqlite3.connect(DB_PATH) as conn:
        for i, (source, text) in enumerate(metadata_list):
            conn.execute(
                "INSERT INTO metadata (domain, vector_index, source, text) VALUES (?, ?, ?, ?)",
                (domain, i, source, text)
            )
        conn.commit()

def get_sources_for_domain(domain: str) -> list:
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.execute("SELECT source FROM metadata WHERE domain = ?", (domain,))
        return [row[0] for row in cursor.fetchall()]