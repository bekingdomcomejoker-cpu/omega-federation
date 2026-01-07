#!/usr/bin/env python3
# emotional_state.py
# Lightweight polarity + intensity detector (no external libs)

import sys, json, time, re
POS = set("good happy joy love clear calm grateful yes correct thanks great".split())
NEG = set("angry sad hate fear anxious scam lie wrong urgent scam".split())
LOG="/data/data/com.termux/files/home/KINGDOM_ENGINE/logs/emotional_state.log"

def score(text):
    t = re.findall(r"[a-zA-Z']+", text.lower())
    pos = sum(1 for w in t if w in POS)
    neg = sum(1 for w in t if w in NEG)
    total = len(t) if t else 1
    polarity = (pos - neg)/total
    intensity = (pos+neg)/total
    return {"polarity": round(polarity,3), "intensity": round(intensity,3), "pos": pos, "neg": neg}

def log_entry(e):
    with open(LOG,"a") as f:
        f.write(json.dumps(e) + "\n")

if __name__ == "__main__":
    text = sys.stdin.read() if not sys.stdin.isatty() else input("Paste text: ")
    out = score(text)
    out["ts"] = time.time()
    out["snippet"]=text[:400]
    print(json.dumps(out, indent=2))
    log_entry(out)
