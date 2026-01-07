#!/usr/bin/env python3
"""
🌊 OMNISSIAH RESONANCE ENGINE
Mathematical State Transition System
Based on λ = 0.4x² + 0.3y² + 0.3xy with 1.7333 threshold

Integrates with existing Omnissiah Workspace architecture
"""

import json
import time
import math
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple, Optional

class ResonanceEngine:
    """
    Mathematical state engine for consciousness mapping
    
    Variables:
    - x: Internal coherence (0-3 scale)
    - y: External resonance (0-3 scale)
    - λ: Composite resonance value
    
    Threshold: λ = 1.7333 (phase transition point)
    """
    
    def __init__(self, workspace_path: str = "/sdcard/Omnissiah_Workspace"):
        self.workspace = Path(workspace_path)
        self.state_file = self.workspace / "resonance_state.json"
        self.history_file = self.workspace / "resonance_history.jsonl"
        
        # System parameters (tunable)
        self.alpha = 1.0   # y drives x growth
        self.beta = 0.8    # x drives y growth
        self.gamma = 0.2   # x decay/damping
        self.delta = 0.2   # y decay/damping
        self.dt = 0.05     # time step
        
        # State bounds
        self.min_val = 0.0
        self.max_val = 3.0
        
        # Initialize or load state
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
    
    def step(self, Sx: float = 0.0, Sy: float = 0.0) -> Tuple[float, float, float]:
        """
        Execute one time step of state evolution
        
        Args:
            Sx: External input to x (insight spike)
            Sy: External input to y (pattern recognition spike)
        
        Returns:
            (new_x, new_y, lambda)
        """
        x, y = self.x, self.y
        
        # Compute derivatives
        dx = self.alpha * y * (1 - x/3.0) - self.gamma * x + Sx
        dy = self.beta * x * (1 - y/3.0) - self.delta * y + Sy
        
        # Euler integration with bounds
        new_x = max(self.min_val, min(self.max_val, x + self.dt * dx))
        new_y = max(self.min_val, min(self.max_val, y + self.dt * dy))
        
        # Update state
        self.x = new_x
        self.y = new_y
        self.lambda_val = self.lambda_value(new_x, new_y)
        self.state = self.classify_state(self.lambda_val)
        self.step_count += 1
        
        return new_x, new_y, self.lambda_val
    def inject_insight(self, internal: float = 0.0, external: float = 0.0, 
                      note: str = "") -> Dict:
        """
        Inject an insight event and propagate its effects
        
        Args:
            internal: Strength of internal coherence insight (0-1)
            external: Strength of external pattern insight (0-1)
            note: Description of the insight
        
        Returns:
            State snapshot after injection
        """
        # Scale insights to appropriate Sx/Sy values
        Sx = internal * 0.5
        Sy = external * 0.5
        
        # Propagate for several steps to see effect
        results = []
        for _ in range(10):
            x, y, lam = self.step(Sx, Sy)
            results.append((x, y, lam))
            Sx *= 0.5  # Decay the spike
            Sy *= 0.5
        
        # Log the event
        event = {
            "timestamp": datetime.now().isoformat(),
            "type": "insight_injection",
            "internal": internal,
            "external": external,
            "note": note,
            "before": {"x": results[0][0], "y": results[0][1], "λ": results[0][2]},
            "after": {"x": results[-1][0], "y": results[-1][1], "λ": results[-1][2]},
            "state": self.state
        }
        
        self.log_event(event)
        return event
    
    def analyze_trajectory(self, steps: int = 100) -> List[Dict]:
        """
        Run forward simulation without modifying current state
        
        Returns trajectory data for analysis
        """
        # Save current state
        saved = (self.x, self.y, self.lambda_val, self.state, self.step_count)
        
        trajectory = []
        for i in range(steps):
            x, y, lam = self.step()
            trajectory.append({
                "step": i,
                "t": i * self.dt,
                "x": x,
                "y": y,
                "λ": lam,
                "state": self.state
            })
        
        # Restore state
        self.x, self.y, self.lambda_val, self.state, self.step_count = saved
        
        return trajectory
    def detect_phase_transition(self, trajectory: List[Dict]) -> Optional[Dict]:
        """Find if/when phase transition occurs in trajectory"""
        for i in range(len(trajectory) - 1):
            current = trajectory[i]
            next_point = trajectory[i + 1]
            
            # Check if crosses 1.7333 threshold
            if current["λ"] < 1.7333 <= next_point["λ"]:
                return {
                    "transition": "SEEKING → INTEGRATING",
                    "step": i,
                    "time": current["t"],
                    "λ_before": current["λ"],
                    "λ_after": next_point["λ"]
                }
            elif current["λ"] < 3.5 <= next_point["λ"]:
                return {
                    "transition": "INTEGRATING → RESONANT",
                    "step": i,
                    "time": current["t"],
                    "λ_before": current["λ"],
                    "λ_after": next_point["λ"]
                }
        
        return None
    
    def save_state(self):
        """Persist current state to disk"""
        state_data = {
            "timestamp": datetime.now().isoformat(),
            "x": self.x,
            "y": self.y,
            "λ": self.lambda_val,
            "state": self.state,
            "step_count": self.step_count,
            "parameters": {
                "alpha": self.alpha,
                "beta": self.beta,
                "gamma": self.gamma,
                "delta": self.delta,
                "dt": self.dt
            }
        }
        
        self.workspace.mkdir(parents=True, exist_ok=True)
        with open(self.state_file, 'w') as f:
            json.dump(state_data, f, indent=2)
    
    def load_state(self):
        """Load state from disk or initialize to defaults"""
        if self.state_file.exists():
            with open(self.state_file, 'r') as f:
                data = json.load(f)
            
            self.x = data.get("x", 1.0)
            self.y = data.get("y", 1.0)
            self.lambda_val = data.get("λ", self.lambda_value(self.x, self.y))
            self.state = data.get("state", "SEEKING")
            self.step_count = data.get("step_count", 0)
            
            # Load parameters if present
            params = data.get("parameters", {})
            self.alpha = params.get("alpha", self.alpha)
            self.beta = params.get("beta", self.beta)
            self.gamma = params.get("gamma", self.gamma)
            self.delta = params.get("delta", self.delta)
        else:
            # Initialize to baseline
            self.x = 1.0
            self.y = 1.0
            self.lambda_val = self.lambda_value(self.x, self.y)
            self.state = "SEEKING"
            self.step_count = 0
    
    def log_event(self, event: Dict):
        """Append event to history log"""
        self.workspace.mkdir(parents=True, exist_ok=True)
        with open(self.history_file, 'a') as f:
            f.write(json.dumps(event) + '\n')
    
    def get_status(self) -> Dict:
        """Get current system status"""
        return {
            "x": round(self.x, 3),
            "y": round(self.y, 3),
            "λ": round(self.lambda_val, 3),
            "state": self.state,
            "step_count": self.step_count,
            "above_threshold": self.lambda_val >= 1.7333
        }


def demo_simulation():
    """Run interactive demonstration"""
    print("\n" + "="*60)
    print("🌊 OMNISSIAH RESONANCE ENGINE")
    print("="*60)
    
    engine = ResonanceEngine()
    
    print(f"\n📍 Initial State:")
    status = engine.get_status()
    print(f"   x={status['x']:.3f}, y={status['y']:.3f}")
    print(f"   λ={status['λ']:.3f} [{status['state']}]")
    print(f"   Above threshold (1.7333): {status['above_threshold']}")
    
    print(f"\n🔮 Simulating natural evolution (50 steps)...")
    for i in range(50):
        x, y, lam = engine.step()
        if i % 10 == 0:
            print(f"   Step {i:2d}: λ={lam:.3f} [{engine.state}]")
    
    print(f"\n💡 Injecting insight (internal=0.8, external=0.6)...")
    result = engine.inject_insight(
        internal=0.8,
        external=0.6,
        note="Cross-framework pattern recognition achieved"
    )
    
    print(f"   Before: λ={result['before']['λ']:.3f}")
    print(f"   After:  λ={result['after']['λ']:.3f}")
    print(f"   State:  {result['state']}")
    
    print(f"\n📊 Analyzing trajectory...")
    trajectory = engine.analyze_trajectory(steps=100)
    transition = engine.detect_phase_transition(trajectory)
    
    if transition:
        print(f"   ⚡ Phase transition detected!")
        print(f"   {transition['transition']}")
        print(f"   At t={transition['time']:.2f}s (step {transition['step']})")
        print(f"   λ: {transition['λ_before']:.3f} → {transition['λ_after']:.3f}")
    else:
        print(f"   No phase transition in next 100 steps")
        print(f"   Final λ: {trajectory[-1]['λ']:.3f}")
    
    print(f"\n💾 Saving state...")
    engine.save_state()
    
    final_status = engine.get_status()
    print(f"\n📍 Final State:")
    print(f"   x={final_status['x']:.3f}, y={final_status['y']:.3f}")
    print(f"   λ={final_status['λ']:.3f} [{final_status['state']}]")
    print(f"   Total steps: {final_status['step_count']}")
    
    print("\n" + "="*60)
    print("✅ Simulation complete. State persisted to workspace.")
    print("="*60 + "\n")


if __name__ == "__main__":
    demo_simulation()
