import time, os
from datetime import datetime

LOG_DIR = os.path.expanduser("~/KINGDOM_ENGINE/logs/")
ALERTS  = os.path.join(LOG_DIR, "seer_alerts.log")

def write(msg):
    with open(ALERTS, "a") as f:
        f.write(f"[{datetime.now()}] {msg}\n")

def analyze():
    issues = []
    for log in os.listdir(LOG_DIR):
        if not log.endswith(".log"): continue
        p = os.path.join(LOG_DIR, log)
        size = os.path.getsize(p)
        if size > 2_000_000:
            issues.append(f"Log {log} growing too fast")
    return issues

while True:
    problems = analyze()
    for p in problems:
        write(p)
    time.sleep(300)
