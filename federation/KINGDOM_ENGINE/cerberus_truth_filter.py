import re
import os
from datetime import datetime

INBOX = os.path.expanduser("~/KINGDOM_ENGINE/inbox/")
OUTBOX = os.path.expanduser("~/KINGDOM_ENGINE/outbox/")
LOG = os.path.expanduser("~/KINGDOM_ENGINE/logs/truth_filter.log")

os.makedirs(OUTBOX, exist_ok=True)

def log(msg):
    with open(LOG, "a") as f:
        f.write(f"[{datetime.now()}] {msg}\n")

def is_noise(text):
    # remove hallucination-like noise patterns (nonsense sequences)
    return bool(re.search(r"[^\w\s\,\.\?\!]", text)) or len(text) < 3

while True:
    for fn in os.listdir(INBOX):
        if not fn.endswith(".txt"): continue

        p = os.path.join(INBOX, fn)
        with open(p) as f: data = f.read()

        if is_noise(data):
            log(f"Filtered noise: {fn}")
            os.remove(p)
            continue

        # truth first: no contradictions
        cleaned = re.sub(r"\b(maybe|probably|i guess)\b", "", data, flags=re.I)

        out = os.path.join(OUTBOX, "tf_" + fn)
        with open(out, "w") as f: f.write(cleaned)

        log(f"Truth-filtered: {fn}")
        os.remove(p)
