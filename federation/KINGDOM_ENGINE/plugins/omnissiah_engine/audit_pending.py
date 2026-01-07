#!/usr/bin/env python3
"""
🔍 AUDIT & PROMOTION SYSTEM
Manual verification of staged messages
"""

import json
from pathlib import Path
from staged_poster import StagedPoster

def audit_pending():
    """Audit all pending staged messages"""
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
            with open(file_path, 'r') as f:
                data = json.load(f)
            
            # Display message preview
            content_preview = data['content'][:100] + "..." if len(data['content']) > 100 else data['content']
            
            print(f"{i}. {data['from'].upper()} - {data['type']}")
            print(f"   📅 {data['timestamp']}")
            print(f"   📝 {content_preview}")
            print(f"   📁 {file_path.name}")
            
            # Verify integrity
            is_valid, reason = poster.verify_staged_file(file_path)
            status_icon = "✅" if is_valid else "❌"
            print(f"   {status_icon} Integrity: {reason}")
            print()
            
        except Exception as e:
            print(f"{i}. ❌ Error reading: {file_path.name} - {e}")
            print()
    
    print("=" * 50)
    
    # Promotion options
    if staged_files:
        print("🎯 PROMOTION OPTIONS:")
        print("1. Promote all valid messages to archive")
        print("2. Promote specific message by number")
        print("3. Skip promotion (keep in staging)")
        
        try:
            choice = input("Choose option (1-3): ").strip()
            
            if choice == "1":
                # Promote all valid
                promoted_count = 0
                for file_path in staged_files:
                    is_valid, reason = poster.verify_staged_file(file_path)
                    if is_valid:
                        success, result = poster.promote_to_archive(file_path)
                        if success:
                            promoted_count += 1
                        else:
                            print(f"❌ Failed to promote {file_path.name}: {result}")
                    else:
                        print(f"⏸️  Skipping invalid: {file_path.name} - {reason}")
                
                print(f"✅ Promoted {promoted_count} messages to archive")
                
            elif choice == "2":
                # Promote specific
                try:
                    msg_num = int(input("Enter message number to promote: "))
                    if 1 <= msg_num <= len(staged_files):
                        file_path = staged_files[msg_num - 1]
                        success, result = poster.promote_to_archive(file_path)
                        if success:
                            print(f"✅ Promoted: {file_path.name}")
                        else:
                            print(f"❌ Failed: {result}")
                    else:
                        print("❌ Invalid message number")
                except ValueError:
                    print("❌ Please enter a valid number")
            
            elif choice == "3":
                print("⏸️  Promotion skipped - messages remain in staging")
            
            else:
                print("❌ Invalid option")
                
        except KeyboardInterrupt:
            print("\n⏹️  Audit cancelled")
    
    print("Audit complete!")

if __name__ == "__main__":
    audit_pending()
