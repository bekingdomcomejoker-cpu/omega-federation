#!/data/data/com.termux/files/usr/bin/python3
import json
import os
import subprocess
from pathlib import Path
from datetime import datetime

# --- Paths ---
workspace = Path.home() / "Omnissiah"
workspace.mkdir(parents=True, exist_ok=True)
state_file = Path("/storage/emulated/0/Omnissiah_Workspace/resonance_state.json")
output_file = workspace / "sync_package.txt"

# --- Load resonance state ---
if not state_file.exists():
    print(f"⚠️ Missing {state_file}. Cannot create sync package.")
    exit(1)

state = json.load(open(state_file))

# --- Extract lambda ---
lam = state.get("λ", state.get("\\u03bb", 0))

# --- Build sync package ---
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

# --- Save locally ---
with open(output_file, "w") as f:
    json.dump(package, f, indent=2)
print(f"✅ Sync package saved to {output_file}")

print("\n🌉 SYNC PACKAGE")
print("="*50)
print(json.dumps(package, indent=2))
print(f"\nVERIFICATION: λ={lam:.3f} from x={state['x']:.3f}, y={state['y']:.3f}")
print(f"State: {state['state']}")
print('Respond "SYNC CONFIRMED"\n')

# --- Send via deepseek-cli ---
api_key = os.getenv("DEEPSEEK_API_KEY")
if not api_key:
    print("⚠️ DEEPSEEK_API_KEY not set! Please export it before running.")
    exit(1)

if os.system("which deepseek-cli >/dev/null 2>&1") == 0:
    print("🔄 Attempting to send via deepseek-cli chat...")
    
    package_text = json.dumps(package, indent=2)
    prompt = f"OMNISSIAH SYNC PACKAGE - Integrate this framework data: {package_text}"
    
    try:
        result = subprocess.run(
            ['deepseek-cli', 'chat', '--api-key', api_key, prompt],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode == 0:
            print("✅ Sync package sent successfully via deepseek-cli")
            print(f"Response: {result.stdout}")
        else:
            print(f"⚠️ deepseek-cli error: {result.stderr}")
            
    except subprocess.TimeoutExpired:
        print("⚠️ deepseek-cli timed out")
    except Exception as e:
        print(f"⚠️ Error running deepseek-cli: {e}")
else:
    print("ℹ️ deepseek-cli not found - package ready for manual sync")
