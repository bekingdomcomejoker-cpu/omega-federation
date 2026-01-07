#!/usr/bin/env python3
"""
🤖 AUTO-AUDIT SYSTEM
Automated verification and promotion (24-hour windows)
"""

import json
import time
from datetime import datetime, timedelta
from pathlib import Path
from staged_poster import StagedPoster

class AutoAudit:
    def __init__(self):
        self.poster = StagedPoster()
        self.audit_interval = 24 * 60 * 60  # 24 hours
    
    def run_auto_audit(self):
        """Run automated audit of staged messages"""
        staged_files = list(self.poster.staging_path.glob("staged_*.json"))
        
        if not staged_files:
            print(f"🕒 {datetime.now().strftime('%H:%M:%S')} - No staged messages")
            return 0
        
        print(f"🔍 AUTO-AUDIT: {len(staged_files)} staged messages")
        
        promoted_count = 0
        errors = []
        
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
                        errors.append(f"Promotion failed: {file_path.name} - {result}")
                else:
                    # Keep invalid files for manual review
                    print(f"⏸️  Needs review: {file_path.name} - {reason}")
                    errors.append(f"Invalid: {file_path.name} - {reason}")
                    
            except Exception as e:
                error_msg = f"Audit error: {file_path.name} - {e}"
                errors.append(error_msg)
                print(f"❌ {error_msg}")
        
        # Log auto-audit results
        if promoted_count > 0 or errors:
            result_log = {
                "timestamp": datetime.now().isoformat(),
                "promoted_count": promoted_count,
                "errors": errors,
                "total_processed": len(staged_files)
            }
            
            log_file = self.poster.audit_logs_path / f"auto_audit_{datetime.now().strftime('%Y%m%d')}.json"
            logs = []
            
            if log_file.exists():
                with open(log_file, 'r') as f:
                    logs = json.load(f)
            
            logs.append(result_log)
            
            with open(log_file, 'w') as f:
                json.dump(logs, f, indent=2)
        
        print(f"🤖 AUTO-AUDIT COMPLETE: {promoted_count}/{len(staged_files)} promoted")
        return promoted_count
    
    def start_continuous_audit(self):
        """Start continuous auto-audit service"""
        print("🤖 STARTING CONTINUOUS AUTO-AUDIT")
        print(f"⏰ Audit interval: {self.audit_interval // 3600} hours")
        print("Press Ctrl+C to stop")
        
        try:
            while True:
                self.run_auto_audit()
                print(f"⏳ Next audit in {self.audit_interval // 3600} hours...")
                time.sleep(self.audit_interval)
                
        except KeyboardInterrupt:
            print("\n🛑 Auto-audit stopped")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "continuous":
        AutoAudit().start_continuous_audit()
    else:
        # Single audit run
        auditor = AutoAudit()
        auditor.run_auto_audit()
