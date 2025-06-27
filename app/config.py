import os

# Path to the project root (parent of app/)
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

VECTOR_DIR = os.path.join(BASE_DIR, "index")
METADATA_DIR = os.path.join(BASE_DIR, "metadata")
DB_PATH = os.path.join(BASE_DIR, "db", "privacy.db")


DOMAIN_INDEXES = {
    "drive": {
        "index": os.path.join(VECTOR_DIR, "drive_index.faiss"),
        "meta": os.path.join(METADATA_DIR, "drive_map.json"),
    },
    "gmail": {
        "index": os.path.join(VECTOR_DIR, "gmail_index.faiss"),
        "meta": os.path.join(METADATA_DIR, "gmail_map.json"),
    },
    "bookmarks": {
        "index": os.path.join(VECTOR_DIR, "bookmarks_index.faiss"),
        "meta": os.path.join(METADATA_DIR, "bookmarks_map.json"),
    },
        "docs": {
        "index": os.path.join(VECTOR_DIR, "docs_index.faiss"),
        "meta": os.path.join(METADATA_DIR, "docs_map.json"),
    },
    "history": {
        "index": os.path.join(VECTOR_DIR, "history_index.faiss"),
        "meta": os.path.join(METADATA_DIR, "history_map.json"),
    },
    "private": {
        "index": os.path.join(VECTOR_DIR, "private_index.faiss"),
        "meta": os.path.join(METADATA_DIR, "private_map.json"),
    },
}
