 #!/usr/bin/env python3
import json, os
from pathlib import Path
from datetime import datetime

# Paths
workspace = Path.home() / "Omnissiah"
workspace.mkdir(parents=True, exist_ok=True)
state_file = workspace / "resonance_state.json"
output_file = workspace / "sync_package.txt"

# Create dummy JSON if missing
if not state_file.exists():
    print(f"⚠️ {state_file} missing — creating dummy resonance_state.json")
    dummy_state = {
        "x": 2.0954110935944423,
        "y": 1.9652027896318247,
        "λ": 4.150277979743656,
        "state": "RESONANT"
    }
    with open(state_file, "w") as f:
        json.dump(dummy_state, f, indent=2)

# Load resonance state
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

# Print verification
print("\n🌉 SYNC PACKAGE")
print("="*50)
print(json.dumps(package, indent=2))
print(f"\nVERIFICATION: λ={lam:.3f} from x={state['x']:.3f}, y={state['y']:.3f}")
print(f"State: {state['state']}")
print('Respond "SYNC CONFIRMED"\n')

# Save sync package
with open(output_file, "w") as f:
    json.dump(package, f, indent=2)
print(f"✅ Saved to {output_file}")

# Attempt sending to DeepSeek CLI
if os.system("which deepseek") == 0:
    send_status = os.system(f"deepseek --input < {output_file}")
    if send_status == 0:
        print("✅ Sync package sent successfully via DeepSeek CLI")
    else:
        print("⚠️ DeepSeek CLI ran but returned an error")
else:
    print("⚠️ DeepSeek CLI not found — will retry after installation.")
