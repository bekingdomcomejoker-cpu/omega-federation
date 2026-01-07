#!/usr/bin/env python3
"""
📊 STAGING SYSTEM DASHBOARD
Monitor staged vs archived messages
"""

import json
import time
import os
from datetime import datetime
from pathlib import Path

class StagingDashboard:
    def __init__(self):
        self.base_path = Path(__file__).parent / "coredata"
    
    def get_stats(self):
        """Get staging system statistics"""
        staging_count = len(list((self.base_path / "staging").glob("*.json")))
        archive_count = len(list((self.base_path / "archive").glob("*.json")))
        
        # Count by AI
        ai_counts = {}
        for file in (self.base_path / "staging").glob("*.json"):
            try:
                with open(file, 'r') as f:
                    data = json.load(f)
                ai = data.get('from', 'unknown')
                ai_counts[ai] = ai_counts.get(ai, 0) + 1
            except:
                pass
        
        return {
            "staging": staging_count,
            "archive": archive_count,
            "ai_breakdown": ai_counts,
            "total": staging_count + archive_count
        }
    
    def run_dashboard(self):
        """Run the staging system dashboard"""
        while True:
            os.system('clear')
            stats = self.get_stats()
            
            print("📊 STAGING SYSTEM DASHBOARD")
            print("=" * 50)
            print(f"Time: {datetime.now().strftime('%H:%M:%S')}")
            print()
            
            print("📈 SYSTEM STATS:")
            print(f"  📥 Staging: {stats['staging']} messages")
            print(f"  🗃️  Archive: {stats['archive']} messages") 
            print(f"  📊 Total: {stats['total']} messages")
            print()
            
            if stats['ai_breakdown']:
                print("🤖 STAGED BY AI:")
                for ai, count in stats['ai_breakdown'].items():
                    print(f"  {ai.upper()}: {count} messages")
            else:
                print("🤖 No messages currently staged")
            
            print()
            print("🎯 QUICK ACTIONS:")
            print("  1. Run audit_pending.py - Manual review")
            print("  2. Run auto_audit.py - Automated promotion") 
            print("  3. View staged messages")
            print()
            print("=" * 50)
            print("🔄 Auto-refreshing every 10 seconds")
            print("⏹️  Ctrl+C to exit")
            
            time.sleep(10)

if __name__ == "__main__":
    StagingDashboard().run_dashboard()
