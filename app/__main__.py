# app/__main__.py

import argparse
from app.updater import update_domain
from app.query import handle_query, search_all_domains  # Ensure this import is correct

def main():
    parser = argparse.ArgumentParser(prog="privacy-firewall-cli")
    subparsers = parser.add_subparsers(dest="command", required=True)

  
    update_parser = subparsers.add_parser("update", help="Update FAISS index for a specific domain")
    update_parser.add_argument("--domain", required=True, help="Domain to update (e.g., drive, gmail, docs, bookmarks, history)")

    

    query_parser = subparsers.add_parser("query", help="Run a privacy check against stored embeddings")
    query_parser.add_argument("--domain", required=True, help="Domain to check against")
    query_parser.add_argument("--text", required=True, help="Text query to evaluate")
    query_parser.add_argument("--user", default="agent_default", help="User or agent ID making the query")

    search_parser = subparsers.add_parser("search", help="Search all domains for semantic match")
    search_parser.add_argument("--text", required=True, help="Text to search")
    search_parser.add_argument("--user", default="agent_default", help="User or agent ID making the search")

    args = parser.parse_args()

    if args.command == "update":
        print(f"🔄 Updating index for domain: {args.domain}")
        update_domain(args.domain)

    elif args.command == "query":
        print(f"🔍 Checking query for domain: {args.domain} by user: {args.user}")
        result = handle_query(args.domain, args.text, user_id=args.user)
        print("🔒 Result:", result)

    elif args.command == "search":
        print(f"🌐 Searching all domains for: '{args.text}' by user: {args.user}")
        result = search_all_domains(args.text, user_id=args.user)
        print("🔎 Global Search Result:", result)

if __name__ == "__main__":
    main()
