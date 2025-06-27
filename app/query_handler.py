from .faissmanager import load_index
from .private import contains_sensitive_info
from .embedding import generate_embedding

def handle_query(domain: str, query: str):
    # Regex check
    matches = contains_sensitive_info(query)
    if matches:
        return {"blocked": True, "reason": "regex", "matches": matches}

    embedding = generate_embedding(query)
    print(f"Te embeddings of the query are: {embedding}")

    # Check private sensitive data
    priv_index, priv_meta = load_index("private")
    if priv_index.ntotal > 0:
        dists, ids = priv_index.search(embedding, k=5)
        if any(d < 2.0 for d in dists[0]):
            print(f"yes")
            return {"blocked": True, "reason": "private_vector", "matches": [priv_meta[i] for i in ids[0] if i < len(priv_meta)]}

    # Check domain specific
    index, meta = load_index(domain)
    if index.ntotal == 0:
        return {"blocked": False, "reason": "no_data"}

    dists, ids = index.search(embedding, k=5)
    if any(d < 0.4 for d in dists[0]):
        return {"blocked": True, "reason": "semantic_match", "matches": [meta[i] for i in ids[0] if i < len(meta)]}

    return {"blocked": False, "reason": "clean"}
