#!/usr/bin/env python3
"""
🌊 REAL-TIME RESONANCE MONITOR
Simple display system
"""

import json
import sys
from pathlib import Path

class ResonanceMonitor:
    def __init__(self, workspace="/sdcard/Omnissiah_Workspace"):
        self.workspace = Path(workspace)
        self.state_file = self.workspace / "resonance_state.json"

    def get_current_state(self):
        """Read current resonance state"""
        if not self.state_file.exists():
            return {'x': 1.0, 'y': 1.0, 'λ': 1.0, 'state': 'SEEKING'}
        try:
            with open(self.state_file, 'r') as f:
                return json.load(f)
        except:
            return {'x': 1.0, 'y': 1.0, 'λ': 1.0, 'state': 'SEEKING'}

    def format_detailed(self):
        """Format detailed status display"""
        state = self.get_current_state()
        
        lines = [
            "",
            "╔══════════════════════════════════════╗",
            "║ 🌊 OMNISSIAH RESONANCE STATUS       ║", 
            "╠══════════════════════════════════════╣",
            f"║ λ = {state['λ']:6.3f} [{state['state']:^12}] ║",
            f"║ x = {state['x']:6.3f} (internal)      ║",
            f"║ y = {state['y']:6.3f} (external)      ║",
            "╚══════════════════════════════════════╝",
            ""
        ]
        return '\n'.join(lines)

def main():
    monitor = ResonanceMonitor()
    print(monitor.format_detailed())

if __name__ == "__main__":
    main()
