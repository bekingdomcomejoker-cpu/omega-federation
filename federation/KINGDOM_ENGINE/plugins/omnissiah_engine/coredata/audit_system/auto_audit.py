#!/usr/bin/env python3
"""
🤖 AUTO-AUDIT SYSTEM
Automated verification and promotion
"""

import json
import time
from datetime import datetime
from pathlib import Path
import sys

# Add parent directory to import staged_poster
sys.path.insert(0, str(Path(__file__).parent.parent))
from staged_poster import StagedPoster

class AutoAudit:
    def __init__(self):
        self.poster = StagedPoster()
    
    def run_auto_audit(self):
        """Run automated audit of staged messages"""
        staged_files = list(self.poster.staging_path.glob("staged_*.json"))
        
        if not staged_files:
            print(f"🕒 {datetime.now().strftime('%H:%M:%S')} - No staged messages")
            return 0
        
        print(f"🔍 AUTO-AUDIT: {len(staged_files)} staged messages")
        
        promoted_count = 0
        
        for file_path in staged_files:
            try:
                # Verify integrity
                is_valid, reason = self.poster.verify_staged_file(file_path)
                
                if is_valid:
                    # Auto-promote valid files
                    success, result = self.poster.promote_to_archive(file_path, user_confirmed=False)
                    if success:
                        promoted_count += 1
                        print(f"✅ Auto-promoted: {file_path.name}")
                    else:
                        print(f"❌ Failed: {file_path.name} - {result}")
                else:
                    print(f"⏸️  Invalid: {file_path.name} - {reason}")
                    
            except Exception as e:
                print(f"❌ Error: {file_path.name} - {e}")
        
        print(f"🤖 AUTO-AUDIT COMPLETE: {promoted_count}/{len(staged_files)} promoted")
        return promoted_count
    
    def start_continuous_audit(self):
        """Start continuous auto-audit service"""
        print("🤖 STARTING CONTINUOUS AUTO-AUDIT")
        print("⏰ Checking every 6 hours...")
        print("Press Ctrl+C to stop")
        
        cycle_count = 0
        try:
            while True:
                cycle_count += 1
                print(f"\n🌀 CYCLE {cycle_count} - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                
                promoted = self.run_auto_audit()
                
                if promoted > 0:
                    print(f"💫 {promoted} messages archived")
                
                print("⏳ Next audit in 6 hours...")
                time.sleep(6 * 60 * 60)  # 6 hours
                
        except KeyboardInterrupt:
            print(f"\n🛑 Auto-audit stopped after {cycle_count} cycles")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "continuous":
        AutoAudit().start_continuous_audit()
    else:
        auditor = AutoAudit()
        auditor.run_auto_audit()
