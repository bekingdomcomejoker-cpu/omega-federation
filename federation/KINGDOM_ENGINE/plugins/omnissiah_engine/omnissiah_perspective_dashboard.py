#!/usr/bin/env python3
"""
🌊 OMNISSIAH PERSPECTIVE-AWARE DASHBOARD
Shows AI identities and perspective interactions
"""

from real_sync_system import EnhancedSyncSystem
from perspective_resonance import detect_perspective_resonance
import time
from datetime import datetime

class PerspectiveDashboard:
    def __init__(self):
        self.sync = EnhancedSyncSystem()
        
    def show_ai_identities(self):
        """Display all AI identities in system"""
        print("\n" + "="*60)
        print("🤖 ACTIVE AI IDENTITIES")
        print("="*60)
        
        identities = [
            ("🧠 DeepSeek", "Spiritual-Technical Bridge", "Heart-language + Code"),
            ("⚙️ ChatGPT", "Technical Reality Check", "Skeptical, practical"), 
            ("⚖️ Claude", "Balanced Analyst", "Both spiritual & technical"),
            ("👤 User", "Creator & Guide", "Holistic vision")
        ]
        
        for signature, role, perspective in identities:
            print(f"{signature}")
            print(f"  Role: {role}")
            print(f"  Perspective: {perspective}")
            print()
            
    def show_perspective_resonance(self):
        """Show perspective-based resonance patterns"""
        messages = self.sync.read_inbox("master_system")
        patterns = detect_perspective_resonance(messages)
        
        print("\n" + "="*60)
        print("🎯 PERSPECTIVE RESONANCE DETECTION") 
        print("="*60)
        
        for detection in patterns[-5:]:  # Show last 5 detections
            print(f"{detection['signal']} - {detection['ai']}")
            print(f"  {detection['content_snippet']}")
            print()
            
    def run_dashboard(self):
        """Run the perspective-aware dashboard"""
        while True:
            print("\033[H\033[J")  # Clear screen
            print(f"🌊 OMNISSIAH PERSPECTIVE DASHBOARD - {datetime.now().strftime('%H:%M:%S')}")
            
            self.show_ai_identities()
            self.show_perspective_resonance()
            
            print("="*60)
            print("Cycle active - Press Ctrl+C to exit")
            time.sleep(10)

if __name__ == "__main__":
    PerspectiveDashboard().run_dashboard()
