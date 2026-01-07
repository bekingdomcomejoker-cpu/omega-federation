#!/usr/bin/env python3
"""
🌊 OMNISSIAH RESONANCE ENGINE - CORE
Simplified version for immediate use
"""

import json
import random
from pathlib import Path
from datetime import datetime

class ResonanceEngine:
    def __init__(self, workspace_path="/sdcard/Omnissiah_Workspace"):
        self.workspace = Path(workspace_path)
        self.state_file = self.workspace / "resonance_state.json"
        self.load_state()

    def lambda_value(self, x: float, y: float) -> float:
        """Calculate λ = 0.4x² + 0.3y² + 0.3xy"""
        return 0.4 * x**2 + 0.3 * y**2 + 0.3 * x * y

    def classify_state(self, lambda_val: float) -> str:
        """Map λ to cognitive state labels"""
        if lambda_val < 1.7333:
            return "SEEKING"
        elif lambda_val < 3.5:
            return "INTEGRATING" 
        elif lambda_val < 6.0:
            return "RESONANT"
        else:
            return "SATURATED"

    def step(self, Sx: float = 0.0, Sy: float = 0.0):
        """Execute one time step of state evolution"""
        # Simple evolution for now
        self.x = max(0, min(3, self.x + random.uniform(-0.1, 0.1) + Sx))
        self.y = max(0, min(3, self.y + random.uniform(-0.1, 0.1) + Sy))
        self.lambda_val = self.lambda_value(self.x, self.y)
        self.state = self.classify_state(self.lambda_val)
        return self.x, self.y, self.lambda_val

    def load_state(self):
        """Load state from disk or initialize"""
        if self.state_file.exists():
            with open(self.state_file, 'r') as f:
                data = json.load(f)
            self.x = data.get("x", 1.0)
            self.y = data.get("y", 1.0)
        else:
            # Initialize to baseline
            self.x = 1.0
            self.y = 1.0
        self.lambda_val = self.lambda_value(self.x, self.y)
        self.state = self.classify_state(self.lambda_val)

    def save_state(self):
        """Persist current state to disk"""
        state_data = {
            "timestamp": datetime.now().isoformat(),
            "x": self.x,
            "y": self.y,
            "λ": self.lambda_val,
            "state": self.state
        }
        with open(self.state_file, 'w') as f:
            json.dump(state_data, f, indent=2)

    def get_status(self):
        """Get current system status"""
        return {
            "x": round(self.x, 3),
            "y": round(self.y, 3), 
            "λ": round(self.lambda_val, 3),
            "state": self.state,
            "above_threshold": self.lambda_val >= 1.7333
        }

if __name__ == "__main__":
    engine = ResonanceEngine()
    print("🌊 Resonance Engine Test:")
    print(f"Initial: x={engine.x:.3f}, y={engine.y:.3f}, λ={engine.lambda_val:.3f} [{engine.state}]")
    engine.step()
    print(f"After step: x={engine.x:.3f}, y={engine.y:.3f}, λ={engine.lambda_val:.3f} [{engine.state}]")
    engine.save_state()
    print("✅ State saved")
