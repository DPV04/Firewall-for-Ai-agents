from .private import contains_sensitive_info
from .faissmanager import load_index, save_index
from .embedding import generate_embedding
from ingestion import drive, bookmarks, g_docs, history, gmail
from .security import log_query ,log_ingested_data #

def update_domain(domain: str):
    index, meta = load_index(domain)
    priv_index, priv_meta = load_index("private")

    if domain == "drive":
        docs, sources = drive.get_drive()
    elif domain == "bookmarks":
        docs, sources = bookmarks.get_bookmarks()
    elif domain == "history":
        docs, sources = history.get_history()
    elif domain == "gmail":
        docs, sources = gmail.fetch_gmail_messages()
    elif domain == "docs":
        docs, sources = g_docs.fetch_google_docs()
    else:
        raise ValueError("Invalid domain")

    new_meta = []
    new_priv_meta = []
    embeddings = []
    priv_embeddings = []

    for doc, source in zip(docs, sources):
        matches = contains_sensitive_info(doc)
        embedding = generate_embedding(doc)

    
        log_ingested_data(domain, source, doc, is_private=bool(matches))


        if matches:
            priv_embeddings.append(embedding)
            new_priv_meta.append((source, doc))
        else:
            embeddings.append(embedding)
            new_meta.append((source, doc))

  
    for e in embeddings:
        index.add(e)
    meta.extend([text for _, text in new_meta])
    save_index(domain, index, new_meta)


    for e in priv_embeddings:
        priv_index.add(e)
    priv_meta.extend([text for _, text in new_priv_meta])
    save_index("private", priv_index, new_priv_meta)

    print(f" Updated domain: {domain} — {len(embeddings)} regular | {len(priv_embeddings)} private sensitive")


