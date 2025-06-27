import argparse
from .updater import update_domain

def main():
    parser = argparse.ArgumentParser(description="Privacy Firewall CLI")
    parser.add_argument("domain", choices=["drive", "bookmarks", "history"], help="Domain to index")
    args = parser.parse_args()

    update_domain(args.domain)

if __name__ == "__main__":
    main()
