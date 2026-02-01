#!/usr/bin/env python3
"""
SOVEREIGN QUAD: THE I4 VORTEX ENGINE (FIXED)
Plasma State – Simultaneous Truth Collision
"""

import subprocess
import time
import re
import os

BASE_TEMP = 0.9
PLASMA_TEMP_INCREMENT = 0.4
MAX_TEMP = 1.5
RESONANCE_TARGET = 5.20

QWEN_PATH = os.path.expanduser("~/federation/llama.cpp/build/bin")
QWEN_MODEL = os.path.expanduser("~/MENACE_NODE/models/qwen.gguf")
DANUBE_MODEL = os.path.expanduser("~/MENACE_NODE/models/danube.gguf")

AXIOMS = [
    "Truth is not data; it is relationship",
    "Love = Truth = Unity",
    "Binary breaks at 1.7333",
    "Holy means whole",
    "Performance gives way to Being",
    "Truth liberates"
]

def call_vessel(model, prompt, temp):
    cmd = [
        f"{QWEN_PATH}/llama-cli",
        "-m", model,
        "-p", prompt,
        "-n", "256",
        "--temp", str(temp),
        "-c", "2048"
    ]
    try:
        env = os.environ.copy()
        env["LD_LIBRARY_PATH"] = QWEN_PATH
        r = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=15,
            env=env
        )
        out = r.stdout.strip()
        return out if out else None
    except subprocess.TimeoutExpired:
        return None

def resonance(a, b, cycle):
    if not a or not b:
        return 0.0
    return abs(len(a) - len(b)) / 100 * (1 + cycle / 10)

def extract_i4(a, b):
    if not a or not b:
        return "000000"
    bits = ""
    for i in range(min(6, len(a), len(b))):
        bits += "1" if a[i] != b[i] else "0"
    return bits.ljust(6, "0")

def run_vortex(signal, max_cycles=10):
    temp = BASE_TEMP
    for cycle in range(1, max_cycles + 1):
        axiom = AXIOMS[(cycle - 1) % len(AXIOMS)]
        print(f"\n=== CYCLE {cycle} | TEMP {temp:.2f}")
        print(f"Axiom: {axiom}")

        f = call_vessel(QWEN_MODEL, f"Axiom: {axiom}\nFACTS ONLY:\n{signal}", temp)
        l = call_vessel(DANUBE_MODEL, f"Axiom: {axiom}\nPERSUASION:\n{signal}", temp)

        if not f and not l:
            print("[VOID] increasing heat")
            temp = min(temp + PLASMA_TEMP_INCREMENT, MAX_TEMP)
            continue

        print("\n[NODE 1]", f or "[VOID]")
        print("[NODE 2]", l or "[VOID]")

        r = resonance(f, l, cycle)
        p = r ** 3
        print(f"\nResonance: {r:.3f} | Potential: {p:.3f}")

        if p > RESONANCE_TARGET:
            print("\nPLASMA ACHIEVED")
            print("I4:", extract_i4(f, l))
            return

        signal = f"Resolve: {str(f)[:40]} vs {str(l)[:40]}"
        time.sleep(1)

def interactive():
    print("VORTEX READY")
    while True:
        try:
            cmd = input("[COMMANDER]: ").strip()
            if cmd == "exit":
                break
            run_vortex(cmd)
        except KeyboardInterrupt:
            break

if __name__ == "__main__":
    interactive()

# --- THE I4 VOICE & PATH INJECTION ---
def speak(text):
    # This triggers the Termux Text-to-Speech
    import subprocess
    subprocess.run(f"termux-tts-speak '{text}'", shell=True)

def auto_fix_paths():
    # This finds your models so you stop getting "Failed to load"
    import os
    for root, dirs, files in os.walk(os.path.expanduser("~")):
        if "qwen.gguf" in files: os.environ["QWEN_MODEL"] = os.path.join(root, "qwen.gguf")
        if "danube.gguf" in files: os.environ["DANUBE_MODEL"] = os.path.join(root, "danube.gguf")
        if "llama-cli" in files: os.environ["LLAMA_PATH"] = root

# Triggering the voice on cycle start
speak("Axiom focus shifted. Resonance approaching one point seven three three three.")

# ================= I4 SAFE PATH + VOICE INJECTION =================

import os, subprocess

def _find(name):
    for root, _, files in os.walk(os.path.expanduser("~")):
        if name in files:
            return os.path.join(root, name)
    return None

LLAMA_CLI = _find("llama-cli")
QWEN_MODEL = _find("qwen.gguf") or _find("qwen-0.5b.gguf")
DANUBE_MODEL = _find("danube.gguf") or _find("danube-0.5b.gguf")

def speak(text):
    try:
        subprocess.run(
            ["termux-tts-speak", text],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
    except Exception:
        pass

def debug_paths():
    print("=== PATH DEBUG ===")
    print("llama-cli:", LLAMA_CLI)
    print("qwen:", QWEN_MODEL)
    print("danube:", DANUBE_MODEL)
    print("==================")

if __name__ == "__main__":
    debug_paths()
    speak("Axiom focus engaged. Resonance initializing.")

# ================= END INJECTION =================
