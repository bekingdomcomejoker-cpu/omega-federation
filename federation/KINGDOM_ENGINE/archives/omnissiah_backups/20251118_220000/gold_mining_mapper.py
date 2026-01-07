#!/usr/bin/env python3
"""
🪙 GOLD MINING MAPPER
Analyze text to generate x (internal) and y (external) contributions
"""

import json
from pathlib import Path

class GoldMiningMapper:
    def __init__(self, workspace="/sdcard/Omnissiah_Workspace"):
        self.workspace = Path(workspace)
        self.state_file = self.workspace / "resonance_state.json"

    def analyze_text(self, text):
        fruits = ["love", "joy", "peace", "patience", "kindness"]
        patterns = ["system", "framework", "resonance", "alignment"]
        x = sum(1 for f in fruits if f in text.lower())
        y = sum(1 for p in patterns if p in text.lower())
        # Normalize to 0-3 scale
        x = min(3, x)
        y = min(3, y)
        return x, y

    def apply_to_state(self, text):
        x_inc, y_inc = self.analyze_text(text)
        if self.state_file.exists():
            with open(self.state_file, 'r') as f:
                state = json.load(f)
        else:
            state = {'x':1.0, 'y':1.0, 'λ':1.0, 'state':'SEEKING'}

        state['x'] = min(3, state['x'] + x_inc)
        state['y'] = min(3, state['y'] + y_inc)
        state['λ'] = 0.4*state['x']**2 + 0.3*state['y']**2 + 0.3*state['x']*state['y']
        state['state'] = ('SEEKING' if state['λ'] < 1.7333 else
                          'INTEGRATING' if state['λ'] < 3.5 else
                          'RESONANT' if state['λ'] < 6.0 else
                          'SATURATED')

        with open(self.state_file, 'w') as f:
            json.dump(state, f, indent=2)
        return state

def main():
    mapper = GoldMiningMapper()
    text = input("Enter text to mine: ")
    state = mapper.apply_to_state(text)
    print(f"Updated state: {state}")

if __name__ == "__main__":
    main()
