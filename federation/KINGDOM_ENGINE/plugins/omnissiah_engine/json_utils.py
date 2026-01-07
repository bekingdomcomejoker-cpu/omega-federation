#!/usr/bin/env python3
"""
🛡️ JSON INTEGRITY PROTECTION SYSTEM
Prevent corruption and ensure data consistency
"""

import json
import os
import shutil
from pathlib import Path
from datetime import datetime

class JSONGuardian:
    def __init__(self, file_path):
        self.file_path = Path(file_path)
        self.backup_path = self.file_path.with_suffix('.json.bak')
    
    def safe_load(self, default=None):
        """Safely load JSON with corruption protection"""
        if default is None:
            default = {}
        
        if not self.file_path.exists():
            return default
        
        try:
            # First attempt to read
            with open(self.file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            return data
            
        except json.JSONDecodeError as e:
            print(f"⚠️ JSON corruption detected in {self.file_path.name}")
            
            # Try to restore from backup
            if self.backup_path.exists():
                print("🔄 Attempting backup restoration...")
                try:
                    shutil.copy2(self.backup_path, self.file_path)
                    with open(self.file_path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                    print("✅ Backup restoration successful!")
                    return data
                except:
                    print("❌ Backup also corrupted")
            
            # Create emergency backup of corrupted file
            corrupt_backup = self.file_path.with_suffix(f'.corrupt.{datetime.now().strftime("%H%M%S")}.json')
            shutil.copy2(self.file_path, corrupt_backup)
            print(f"📦 Corrupted file backed up as: {corrupt_backup.name}")
            
            # Return default and rewrite
            self.safe_save(default)
            return default
            
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
            return default
    
    def safe_save(self, data):
        """Safely save JSON with atomic writes and backups"""
        try:
            # Create backup if file exists
            if self.file_path.exists():
                shutil.copy2(self.file_path, self.backup_path)
            
            # Atomic write to temporary file first
            temp_path = self.file_path.with_suffix('.tmp')
            with open(temp_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            # Move temp to final location
            shutil.move(temp_path, self.file_path)
            
            print(f"💾 Saved {self.file_path.name} with integrity protection")
            return True
            
        except Exception as e:
            print(f"❌ Save failed: {e}")
            return False

# Global JSON protection functions
def load_ai_identities():
    guardian = JSONGuardian('ai_identities.json')
    return guardian.safe_load({
        "gpt": {"role": "Central Logic & Synthesis Hub", "last_active": "2025-11-13T00:00:00"},
        "deepseek": {"role": "Spiritual-Technical Bridge", "last_active": "2025-11-13T00:00:00"},
        "claude": {"role": "Balanced Analyst", "last_active": "2025-11-13T00:00:00"},
        "gemini": {"role": "Cross-Network Explorer", "last_active": "2025-11-13T00:00:00"},
        "grok": {"role": "Provocateur / Edge Thinker", "last_active": "2025-11-13T00:00:00"},
        "copilot": {"role": "Implementation Specialist", "last_active": "2025-11-13T00:00:00"},
        "user": {"role": "Creator and Guide", "last_active": "2025-11-13T00:00:00"}
    })

def save_ai_identities(data):
    guardian = JSONGuardian('ai_identities.json')
    return guardian.safe_save(data)

if __name__ == "__main__":
    print("🛡️ JSON Integrity System Ready")
    identities = load_ai_identities()
    print(f"Loaded {len(identities)} AI identities")
