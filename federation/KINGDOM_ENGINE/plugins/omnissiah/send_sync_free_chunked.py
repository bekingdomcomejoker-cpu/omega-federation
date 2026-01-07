#!/data/data/com.termux/files/usr/bin/python3
import json
import os
import subprocess
from pathlib import Path
from datetime import datetime
import textwrap

# Paths
workspace = Path.home() / "Omnissiah"
workspace.mkdir(parents=True, exist_ok=True)
state_file = Path("/storage/emulated/0/Omnissiah_Workspace/resonance_state.json")
output_file = workspace / "sync_package.txt"

# Load resonance state
if not state_file.exists():
    print(f"⚠️ Missing {state_file}. Cannot create sync package.")
    exit(1)

state = json.load(open(state_file))
lam = state.get("λ", state.get("\\u03bb", 0))

# Build sync package
package = {
    "version": "1.0",
    "timestamp": datetime.now().isoformat(),
    "resonance_state": {
        "x": state["x"],
        "y": state["y"],
        "lambda": lam,
        "state_label": state["state"],
        "above_threshold": lam >= 1.7333
    },
    "formula": {
        "expression": "λ = 0.4*x^2 + 0.3*y^2 + 0.3*x*y",
        "threshold": 1.7333
    }
}

# Save locally
with open(output_file, "w") as f:
    json.dump(package, f, indent=2)
print(f"✅ Sync package saved to {output_file}")

# Convert package to string and split into chunks
package_text = json.dumps(package, indent=2)
chunks = textwrap.wrap(package_text, width=800)  # 800 chars per chunk to stay free-tier safe

# Send each chunk via deepseek-cli chat
if os.system("which deepseek-cli >/dev/null 2>&1") == 0:
    print("🔄 Sending summary to DeepSeek CLI (free-tier mode)...")
    for i, chunk in enumerate(chunks):
        prompt = f"OMNISSIAH SYNC PACKAGE CHUNK {i+1}/{len(chunks)}:\n{chunk}"
        try:
            result = subprocess.run(
                ['deepseek-cli', 'chat', prompt],
                capture_output=True,
                text=True,
                timeout=20
            )
            if result.returncode == 0:
                print(f"✅ Chunk {i+1} sent successfully")
            else:
                print(f"⚠️ Chunk {i+1} error: {result.stderr}")
        except subprocess.TimeoutExpired:
            print(f"⚠️ Chunk {i+1} timed out")
        except Exception as e:
            print(f"⚠️ Chunk {i+1} exception: {e}")
else:
    print("ℹ️ deepseek-cli not found - package ready for manual sync")

print("\n🌉 SYNC PACKAGE SENT IN CHUNKS (Free-tier compatible)")
