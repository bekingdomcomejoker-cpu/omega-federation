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
output_file = workspace / "sync_package.txt"

# Load resonance state
if not state_file.exists():
    print(f"⚠️ Missing {state_file}. Cannot create sync package.")
    exit(1)

state = json.load(open(state_file))

lam = state.get("λ", state.get("\\u03bb", 0))

# Build sync package locally
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

# Free-tier-friendly prompt
prompt = f"OMNISSIAH SYNC SUMMARY: λ={lam:.3f}, x={state['x']:.3f}, y={state['y']:.3f}, State={state['state']}"

# Attempt to send concise summary to DeepSeek CLI
if os.system("which deepseek-cli >/dev/null 2>&1") == 0:
    api_key = os.environ.get("DEEPSEEK_API_KEY", "").strip()
    if not api_key:
        print("⚠️ No DEEPSEEK_API_KEY set. Add it via export DEEPSEEK_API_KEY='YOUR_KEY'")
    else:
        print("🔄 Sending summary to DeepSeek CLI (free-tier mode)...")
        try:
            result = subprocess.run(
                ['deepseek-cli', 'chat', '--api-key', api_key, prompt],
                capture_output=True,
                text=True,
                timeout=20
            )
            if result.returncode == 0:
                print("✅ Summary sent successfully!")
                print(f"Response: {result.stdout.strip()}")
            else:
                print(f"⚠️ deepseek-cli error: {result.stderr.strip()}")
        except Exception as e:
            print(f"⚠️ Error running deepseek-cli: {e}")
else:
    print("ℹ️ deepseek-cli not found - package ready for manual sync")

