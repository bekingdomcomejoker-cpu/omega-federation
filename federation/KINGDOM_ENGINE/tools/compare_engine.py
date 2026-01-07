#!/usr/bin/env python3
"""
compare_engine.py
Run a single prompt through:
 - cherubim_engine.py (the Merkabah controller)
 - head9_missionary.py (external LLM simulator)
 - covenant_engine.py (axiom checks)
 - harmony_ridge.py (harmony score)
and print side-by-side results.

Usage:
  python3 compare_engine.py "Your prompt here"
"""
import subprocess, shlex, json, sys, os, time

ROOT = os.path.expanduser("~/KINGDOM_ENGINE")
AN = os.path.join(ROOT, "analyzers")
CHERUBIM = os.path.join(AN, "cherubim_engine.py")
MISSIONARY = os.path.join(ROOT, "head9_missionary.py")
COVENANT = os.path.join(AN, "covenant_engine.py")
HARMONY = os.path.join(AN, "harmony_ridge.py")

def run_python(script_path, input_text):
    if not os.path.exists(script_path):
        return {"error": f"Missing: {script_path}"}
    try:
        p = subprocess.Popen(shlex.split(f"python3 {script_path}"),
                             stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = p.communicate(input_text.encode("utf-8"))
        out_s = out.decode("utf-8").strip()
        err_s = err.decode("utf-8").strip()
        try:
            parsed = json.loads(out_s) if out_s else {}
        except Exception:
            parsed = {"raw": out_s}
        return {"code": p.returncode, "output": parsed, "stderr": err_s}
    except Exception as e:
        return {"error": str(e)}

def short(s, n=140):
    s = str(s)
    return (s[:n]+"...") if len(s)>n else s

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 compare_engine.py \"Your prompt here\"")
        sys.exit(1)
    prompt = sys.argv[1]

    print("="*80)
    print("Prompt:")
    print(prompt)
    print("="*80)
    t0 = time.time()

    # 1) Covenant check
    covenant = run_python(COVENANT, prompt)
    print("\n[1] Covenant Engine (Axiom check)")
    print(json.dumps(covenant, indent=2, default=str))

    # 2) Direct Missionary (simulate Gemini) — what the external AI would return raw
    missionary = run_python(MISSIONARY, prompt)
    print("\n[2] Direct Missionary (external LLM simulator)")
    print(json.dumps(missionary, indent=2, default=str))

    # 3) Cherubim (the Merkabah controller) — this will call the Missionary when vector==EAGLE
    cherubim = run_python(CHERUBIM, prompt)
    print("\n[3] Cherubim (Merkabah controller) decision")
    print(json.dumps(cherubim, indent=2, default=str))

    # 4) Harmony Ridge (score the prompt)
    harmony = run_python(HARMONY, prompt)
    print("\n[4] Harmony Ridge (resonance/harmony score)")
    print(json.dumps(harmony, indent=2, default=str))

    print("\nElapsed:", round(time.time()-t0, 2), "seconds")
    print("="*80)
    # Quick readable side-by-side summary
    print("\nSUMMARY:")
    cov_status = covenant.get("output", {}).get("status") if isinstance(covenant.get("output",{}), dict) else covenant.get("output")
    cher_face = cherubim.get("output", {}).get("face") if isinstance(cherubim.get("output",{}), dict) else None
    cher_action = cherubim.get("output", {}).get("routing_action") if isinstance(cherubim.get("output",{}), dict) else None
    mission_raw = missionary.get("output", {}).get("llm_response") if isinstance(missionary.get("output",{}), dict) else missionary.get("output")
    harmony_score = harmony.get("output", {}).get("harmony_score") if isinstance(harmony.get("output",{}), dict) else None

    print(f"  Covenant: {cov_status}")
    print(f"  Cherubim face/action: {cher_face} / {cher_action}")
    print(f"  Missionary (sim) raw reply: {short(mission_raw,200)}")
    print(f"  Harmony score: {harmony_score}")
    print()
    print("Log locations (tail these to observe live routing):")
    print("  Gatekeeper log: ~/KINGDOM_ENGINE/MEGA/logs/gatekeeper.log")
    print("  Cherubim log:   ~/KINGDOM_ENGINE/logs/cherubim.log")
    print("  Missionary log: ~/KINGDOM_ENGINE/logs/head9_missionary.log")
    print("  Head1 log:      ~/KINGDOM_ENGINE/logs/head1_clipboard.log")
    print()
    print("If Gatekeeper accepts the file it will go to: ~/KINGDOM_ENGINE/MEGA/processed/accepted/")
    print("If Gatekeeper quarantines: ~/KINGDOM_ENGINE/MEGA/processed/quarantine/")
    print("="*80)

if __name__ == "__main__":
    main()
