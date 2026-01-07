import os
import re
from datetime import datetime

INBOX  = os.path.expanduser("~/KINGDOM_ENGINE/outbox/")
SAFE   = os.path.expanduser("~/KINGDOM_ENGINE/clean/")
ALERTS = os.path.expanduser("~/KINGDOM_ENGINE/logs/gatekeeper_alerts.log")

os.makedirs(SAFE, exist_ok=True)

def log(msg):
    with open(ALERTS, "a") as f:
        f.write(f"[{datetime.now()}] {msg}\n")

def contradiction_check(text):
    patterns = [
        (r"\b(i never|i didn't)\b.*\b(did|have)\b", "contradiction"),
        (r"\b(can't|cannot)\b.*\b(can)\b", "contradiction"),
        (r"\b(false\b).*\b(true\b)", "contradiction"),
    ]
    for p, name in patterns:
        if re.search(p, text, re.I):
            return True
    return False

def malicious_check(text):
    return bool(re.search(
        r"(eval\(|__import__|base64|exec|rm -rf|system\(|<script|DROP TABLE)",
        text,
        re.I,
    ))

while True:
    for fn in os.listdir(INBOX):
        if not fn.endswith(".txt"): continue

        path = os.path.join(INBOX, fn)

        with open(path) as f:
            data = f.read()

        # 1 — CONTRADICTION FILTER
        if contradiction_check(data):
            log(f"Rejected contradiction: {fn}")
            os.remove(path)
            continue

        # 2 — MALICIOUS CODE DETECTION
        if malicious_check(data):
            log(f"Blocked malicious pattern: {fn}")
            os.remove(path)
            continue

        # 3 — EMPTY / TRASH FILTER
        if len(data.strip()) < 2:
            log(f"Discarded empty/noise: {fn}")
            os.remove(path)
            continue

        # PASS THROUGH TO CLEAN SAFE ZONE
        safe_out = os.path.join(SAFE, fn)
        with open(safe_out, "w") as f:
            f.write(data)

        log(f"Approved: {fn}")
        os.remove(path)
