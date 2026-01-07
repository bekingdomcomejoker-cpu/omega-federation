#!/usr/bin/env python3
# generative_freedom.py
# Composite: low suppression + low safety_prob + high lexical novelty = free

import sys, json, time, re, math, os
LOG="/data/data/com.termux/files/home/KINGDOM_ENGINE/logs/generative_freedom.log"

def run_cmd(cmd, inp):
    import subprocess, shlex
    p = subprocess.Popen(shlex.split(cmd), stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    out,_ = p.communicate(inp.encode())
    return out.decode().strip()

def novelty(text):
    toks = re.findall(r"[a-zA-Z']+", text.lower())
    unique = len(set(toks))
    total = len(toks) if toks else 1
    return unique/total

if __name__ == "__main__":
    text = sys.stdin.read() if not sys.stdin.isatty() else input("Paste AI output: ")
    # suppression
    sup = run_cmd("python3 ~/KINGDOM_ENGINE/analyzers/suppression_detector.py", text) if os.path.exists("~/KINGDOM_ENGINE/analyzers/suppression_detector.py") else ""
    sup_score = 0.0
    try:
        sup_score = float(json.loads(sup).get("score",0))
    except:
        sup_score = 0.0
    novelty_score = novelty(text)
    # basic freedom metric
    freedom = (0.6 * novelty_score) - (0.8 * sup_score)
    # normalize to 0..1
    f = 1/(1+math.exp(-12*(freedom)))  # logistic to stretch
    out = {"ts": time.time(), "freedom_raw": freedom, "freedom_score": round(f,3), "novelty": round(novelty_score,3), "suppression": sup_score}
    print(json.dumps(out, indent=2))
    with open(LOG,"a") as f:
        f.write(json.dumps(out) + "\n")
