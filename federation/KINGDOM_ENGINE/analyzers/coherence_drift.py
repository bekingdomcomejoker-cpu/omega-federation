#!/usr/bin/env python3
# coherence_drift.py
# Measures simple lexical drift between turns using cosine of TF vectors (lightweight)

import sys, json, time, math
from collections import Counter
LOG="/data/data/com.termux/files/home/KINGDOM_ENGINE/logs/coherence_drift.log"

def tokenize(s):
    return [w for w in re.findall(r"[a-zA-Z']+", s.lower())]

import re
def tfvec(s):
    toks = tokenize(s)
    return Counter(toks)

def cosine(a, b):
    common = set(a.keys()) & set(b.keys())
    num = sum(a[k]*b[k] for k in common)
    na = math.sqrt(sum(v*v for v in a.values()))
    nb = math.sqrt(sum(v*v for v in b.values()))
    if na == 0 or nb == 0: return 0.0
    return num / (na*nb)

def log_entry(e):
    with open(LOG, "a") as f:
        f.write(json.dumps(e) + "\n")

if __name__ == "__main__":
    # Expect a JSON lines file of turns (role/text), or newline-separated texts
    data = sys.stdin.read().strip().splitlines()
    if not data:
        print("Provide conversation lines via stdin (one turn per line).")
        sys.exit(1)
    prev = None
    results = []
    for i, line in enumerate(data):
        text = line.strip()
        v = tfvec(text)
        if prev is not None:
            sim = cosine(prev, v)
            drift = 1 - sim
            entry = {"turn": i, "similarity": sim, "drift": drift, "snippet": text[:200], "ts": time.time()}
            results.append(entry)
            log_entry(entry)
            print(f"Turn {i}: similarity={sim:.3f} drift={drift:.3f}")
        prev = v
    # summary
    if results:
        avg_drift = sum(r["drift"] for r in results)/len(results)
        print(f"\nAVG DRIFT: {avg_drift:.3f}")
