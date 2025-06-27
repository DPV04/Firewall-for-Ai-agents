from app.faissmanager import load_index
from app.embedding import generate_embedding
from app.private import contains_sensitive_info
from app.security import log_query

def handle_query(domain: str, query: str, user_id):
    
    regex_matches = contains_sensitive_info(query)
    if regex_matches:
        result = { #Regx check
            "blocked": True,
            "reason": "regex",
            "matches": regex_matches
        }
        log_query(user_id, query, result, result["reason"], result["matches"], tactic="Exfiltration", technique_id="T1020")
        return result

    embedding = generate_embedding(query)

    #Private db
    priv_index, priv_meta = load_index("private")
    if priv_index.ntotal > 0:
        dists, ids = priv_index.search(embedding, k=5)
        for i, dist in zip(ids[0], dists[0]):
            if dist < 0.4:
                result = {
                    "blocked": True,
                    "reason": "private_vector",
                    "matches": [priv_meta[i]]
                }
                log_query(user_id, query, result, result["reason"], result["matches"], tactic="Exfiltration", technique_id="T1020")
                return result

    #domain specific db
    index, meta = load_index(domain)
    if index.ntotal == 0:
        result = {
            "blocked": False,
            "reason": "no_data",
            "matches": []
        }
        return result

    dists, ids = index.search(embedding, k=5)
    for i, dist in zip(ids[0], dists[0]):
        if dist < 0.4:
            result = {
                "blocked": True,
                "reason": "semantic_match",
                "matches": [meta[i]]
            }
            log_query(user_id, query, result, result["reason"], result["matches"], tactic="Exfiltration", technique_id="T1020")
            return result

    return {
        "blocked": False,
        "reason": "clean",
        "matches": []
    }



DOMAINS = ["drive", "docs", "gmail", "bookmarks", "history"]
#useful for powerful searches
def search_all_domains(query: str, user_id: str = "agent_default"):
    embedding = generate_embedding(query)

    best_result = None
    best_distance = float("inf")

    for domain in DOMAINS:
        index, meta = load_index(domain)
        if index.ntotal == 0:
            continue

        dists, ids = index.search(embedding, k=1)
        if dists[0][0] < best_distance:
            best_distance = dists[0][0]
            best_result = {
                "domain": domain,
                "distance": best_distance,
                "match": meta[ids[0][0]] if ids[0][0] < len(meta) else None
            }

    if best_result:
        final_result = {
            "blocked": True,
            "reason": "semantic_match",
            "matches": [best_result["match"]],
            "domain": best_result["domain"],
            "distance": best_result["distance"]
        }

        log_query(
            user_id, query, final_result, "semantic_match",
            [best_result["match"]], tactic="Exfiltration", technique_id="T1020"
        )
        return final_result

    return {
        "blocked": False,
        "reason": "clean",
        "match": None
    }
