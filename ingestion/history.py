# app/ingestion/browsing_history_ingestion.py

import os
import sqlite3
import shutil
import tempfile
from app.faissmanager import get_sources_for_domain

def get_history():
    original_path = os.path.expanduser("~/.config/google-chrome/Default/History")

    if not os.path.exists(original_path):
        print(" Chrome history file not found.")
        return [], []

 
    temp_path = tempfile.NamedTemporaryFile(delete=False).name
    shutil.copy2(original_path, temp_path)

    existing_sources = set(get_sources_for_domain("history"))

    try:
        con = sqlite3.connect(temp_path)
        cursor = con.cursor()
        cursor.execute("SELECT url, title FROM urls ORDER BY last_visit_time DESC LIMIT 100;")
        rows = cursor.fetchall()
        con.close()
    except Exception as e:
        print(f" Error reading Chrome history: {e}")
        return [], []
    finally:
        os.remove(temp_path)

    texts, sources = [], []
    for url, title in rows:
        if not title:
            continue
        source = url.strip()
        if source in existing_sources:
            continue
        texts.append(f"{title} {url}")
        sources.append(source)

    return texts, sources
