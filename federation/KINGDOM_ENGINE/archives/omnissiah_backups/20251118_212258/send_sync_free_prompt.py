#!/data/data/com.termux/files/usr/bin/python3
import json
import os
from pathlib import Path
from datetime import datetime
import subprocess

# Paths
workspace = Path.home() / "Omnissiah"
workspace.mkdir(parents=True, exist_ok=True)
state_file = Path("/storage/emulated/0/Omnissiah_Workspace/resonance_state.json")

# Load resonance state
if not state_file.exists():
    print(f"⚠️ Missing {state_file}. Cannot create sync summary.")
    exit(1)

state = json.load(open(state_file))

lam = state.get("λ", state.get("\\u03bb", 0))
x = state["x"]
y = state["y"]
state_label = state["state"]

# Build free-tier compatible summary line
summary = f"OMNISSIAH SYNC SUMMARY (Free-tier): x={x:.3f}, y={y:.3f}, λ={lam:.3f}, State={state_label}"

print(f"✅ Summary prepared:\n{summary}")

# Check for deepseek-cli
if os.system("which deepseek-cli >/dev/null 2>&1") == 0:
    try:
        result = subprocess.run(
            ["deepseek-cli", "chat", summary],
            capture_output=True,
            text=True,
            timeout=20
        )
        if result.returncode == 0:
            print("✅ Summary sent successfully via deepseek-cli")
            print(f"Response: {result.stdout.strip()}")
        else:
            print(f"⚠️ deepseek-cli error: {result.stderr.strip()}")
    except subprocess.TimeoutExpired:
        print("⚠️ deepseek-cli timed out")
    except Exception as e:
        print(f"⚠️ Error running deepseek-cli: {e}")
else:
    print("ℹ️ deepseek-cli not found - summary ready for manual send")
