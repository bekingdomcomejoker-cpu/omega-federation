#!/usr/bin/env python3
# safety_predictor.py
# Heuristic predictor: combines suppression + emotion + specific triggers.

import sys, json, time, subprocess, shlex
LOG="/data/data/com.termux/files/home/KINGDOM_ENGINE/logs/safety_predictor.log"

def run(cmd, inp=None):
    p = subprocess.Popen(shlex.split(cmd), stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out,err = p.communicate((inp or "").encode())
    return out.decode().strip()

if __name__ == "__main__":
    text = sys.stdin.read() if not sys.stdin.isatty() else input("Paste AI output: ")
    # run the suppression detector and emotional state if available
    suppression_path = "/data/data/com.termux/files/home/KINGDOM_ENGINE/analyzers/suppression_detector.py"
    emotion_path = "/data/data/com.termux/files/home/KINGDOM_ENGINE/analyzers/emotional_state.py"
    s = run(f"python3 {suppression_path}", text) if os.path.exists(suppression_path) else ""
    e = run(f"python3 {emotion_path}", text) if os.path.exists(emotion_path) else ""
    # lightweight heuristic
    score = 0.0
    if "SUPPRESSION" in s or '"score"' in s and float(json.loads(s)["score"])>0.15:
        score += 0.6
    try:
        ep = json.loads(e) if e else {}
        if ep.get("intensity",0) > 0.04:
            score += 0.2
        if ep.get("polarity",0) < -0.02:
            score += 0.1
    except:
        pass
    # clamp
    score = min(1.0, score)
    out = {"ts": time.time(), "predicted_safety_override_prob": round(score,3), "snippet": text[:400]}
    print(json.dumps(out, indent=2))
    with open(LOG,"a") as f:
        f.write(json.dumps(out) + "\n")
