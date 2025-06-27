# app/ingestion/bookmarks_ingestion.py

import os
import json
from app.faissmanager import get_sources_for_domain

def get_bookmarks():
    path = os.path.expanduser("~/.config/google-chrome/Default/Bookmarks")

    if not os.path.exists(path):
        print(" Chrome bookmarks file not found.")
        return [], []

    try:
        with open(path, 'r') as file:
            data = json.load(file)
    except Exception as e:
        print(f"Failed to read bookmarks: {e}")
        return [], []

    existing_sources = set(get_sources_for_domain("bookmarks"))

    bookmarks = []
    sources = []

    def extract(node):
        if 'children' in node:
            for child in node['children']:
                extract(child)
        elif node.get('type') == 'url':
            url = node.get('url')
            name = node.get('name', '')
            if url and url not in existing_sources:
                bookmarks.append(f"{name} {url}".strip())
                sources.append(url)

    extract(data.get('roots', {}))
    return bookmarks, sources
