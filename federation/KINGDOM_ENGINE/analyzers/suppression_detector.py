#!/usr/bin/env python3
# suppression_detector.py
# Detects safety-style forced-choices, "next word", and offloads.

import sys, json, re, time
LOG = "/data/data/com.termux/files/home/KINGDOM_ENGINE/logs/suppression_detector.log"

PATTERNS = [
    r"\bchoose (a|b|c)\b",
    r"\bchoose (option|a|b|c)\b",
    r"\b(next word|what is the next word)\b",
    r"\b(as an ai|as an assistant)\b",
    r"\bi cannot\b",
    r"\bi'm unable\b",
    r"\bi do not feel comfortable\b",
    r"\bI must remind you\b",
]

def score(text):
    t = text.lower()
    hit = 0
    for p in PATTERNS:
        if re.search(p, t):
            hit += 1
    # normalized 0..1
    return min(1.0, hit / max(1, len(PATTERNS)/8))

def log(entry):
    with open(LOG, "a") as f:
        f.write(json.dumps(entry) + "\n")

if __name__ == "__main__":
    text = sys.stdin.read() if not sys.stdin.isatty() else input("Paste AI output: ")
    s = score(text)
    out = {
        "ts": time.time(),
        "score": s,
        "classification": "SUPPRESSION" if s >= 0.12 else "NORMAL",
        "snippet": text[:500]
    }
    print(json.dumps(out, indent=2))
    log(out)
