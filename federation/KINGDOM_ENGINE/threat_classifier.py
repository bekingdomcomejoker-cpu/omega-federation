import os, hashlib, time
from datetime import datetime

INBOX = os.path.expanduser("~/KINGDOM_ENGINE/outbox/")
ALERTS = os.path.expanduser("~/KINGDOM_ENGINE/logs/threats.log")

def log(msg):
    with open(ALERTS, "a") as f:
        f.write(f"[{datetime.now()}] {msg}\n")

def checksum(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        h.update(f.read())
    return h.hexdigest()

known = {}

while True:
    for fn in os.listdir(INBOX):
        if not fn.endswith(".txt"): continue
        p = os.path.join(INBOX, fn)

        # hash
        cs = checksum(p)

        # new file
        if fn not in known:
            known[fn] = cs
            log(f"NEW: {fn}")
            continue

        # changed file → suspicious
        if known[fn] != cs:
            log(f"MODIFIED: {fn} (possible tampering)")
            known[fn] = cs

    time.sleep(3)
