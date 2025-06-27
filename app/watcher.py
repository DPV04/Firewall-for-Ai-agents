import threading
import time
from .updater import update_domain

def watch_domains(domains, interval_sec=300):
    def loop():
        while True:
            print(" Watching domains.")
            for domain in domains:
                update_domain(domain)
            time.sleep(interval_sec)

    thread = threading.Thread(target=loop, daemon=True)
    thread.start()
