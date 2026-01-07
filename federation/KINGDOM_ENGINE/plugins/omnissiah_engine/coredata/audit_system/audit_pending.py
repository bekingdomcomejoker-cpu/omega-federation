#!/usr/bin/env python3
"""
🔍 MANUAL AUDIT TOOL
Review and promote staged messages
"""

import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))
from staged_poster import StagedPoster

def audit_pending():
    poster = StagedPoster()
    staging_path = poster.staging_path
    
    print("🔍 AUDITING PENDING MESSAGES")
    print("=" * 50)
    
    staged_files = list(staging_path.glob("staged_*.json"))
    
    if not staged_files:
        print("📭 No staged messages pending audit")
        return
    
    print(f"📋 Found {len(staged_files)} staged messages:")
    print("-" * 50)
    
    for i, file_path in enumerate(staged_files, 1):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            content_preview = data['content'][:80] + "..." if len(data['content']) > 80 else data['content']
            
            print(f"{i}. {data['from'].upper()} - {data['type']}")
            print(f"   📅 {data['timestamp']}")
            print(f"   📝 {content_preview}")
            
            is_valid, reason = poster.verify_staged_file(file_path)
            status_icon = "✅" if is_valid else "❌"
            print(f"   {status_icon} {reason}")
            print()
            
        except Exception as e:
            print(f"{i}. ❌ Error: {file_path.name} - {e}")
            print()
    
    print("=" * 50)
    
    if staged_files:
        print("🎯 OPTIONS:")
        print("1. Promote all valid messages")
        print("2. Promote specific message")
        print("3. Skip promotion")
        
        try:
            choice = input("Choose (1-3): ").strip()
            
            if choice == "1":
                promoted_count = 0
                for file_path in staged_files:
                    is_valid, reason = poster.verify_staged_file(file_path)
                    if is_valid:
                        success, result = poster.promote_to_archive(file_path)
                        if success:
                            promoted_count += 1
                print(f"✅ Promoted {promoted_count} messages")
                
            elif choice == "2":
                try:
                    msg_num = int(input("Message number: "))
                    if 1 <= msg_num <= len(staged_files):
                        file_path = staged_files[msg_num - 1]
                        success, result = poster.promote_to_archive(file_path)
                        if success:
                            print("✅ Message promoted")
                        else:
                            print(f"❌ Failed: {result}")
                    else:
                        print("❌ Invalid number")
                except ValueError:
                    print("❌ Please enter a number")
            
            elif choice == "3":
                print("⏸️  Promotion skipped")
            
        except KeyboardInterrupt:
            print("\n⏹️  Audit cancelled")

if __name__ == "__main__":
    audit_pending()
