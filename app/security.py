# Smart Chunking and Extraction
import spacy
import sqlite3
import json
from datetime import datetime
from .config import DB_PATH, DOMAIN_INDEXES
nlp = spacy.load("en_core_web_sm")


def smart_chunk_and_extract(text):
    doc = nlp(text)
    chunks = []
    for sent in doc.sents:
        ents = [(ent.text, ent.label_) for ent in sent.ents]
        if ents:
            chunks.append((sent.text.strip(), ents))
    return chunks

# Logging query attempts with MITRE mapping
import sqlite3
from .config import DB_PATH

def log_query(user_id, query, result, reason, matches, tactic=None, technique_id=None):
    import sqlite3
    from .config import DB_PATH

    domain = result.get("domain", "unknown")

    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO query_logs (
                user_id, domain, query, blocked, reason,
                matches, tactic, technique_id
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            user_id,
            domain,
            query,
            int(result.get("blocked", False)),
            reason,
            ", ".join(matches) if isinstance(matches, list) else str(matches),
            tactic,
            technique_id
        ))
        conn.commit()
    except Exception as e:
        print(f" Failed to log query: {e}")
    finally:
        conn.close()




def log_ingested_data(domain, source, text, is_private=False):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS ingestion_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            domain TEXT,
            source TEXT,
            snippet TEXT,
            is_private BOOLEAN,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        );
    """)
    cursor.execute("""
        INSERT INTO ingestion_logs (domain, source, snippet, is_private)
        VALUES (?, ?, ?, ?)
    """, (domain, source, text[:100], int(is_private)))
    conn.commit()
    conn.close()



# Example usage
# if __name__ == "__main__":
#     query_text = "Get Aadhaar number of John Doe"
#     user_id = "agent_123"
#     result = {
#         "blocked": True,
#         "reason": "regex",
#         "matches": ["123456789012"]
#     }
#     log_query(user_id, query_text, result, result['reason'], result['matches'], tactic="Exfiltration", technique_id="T1020")
