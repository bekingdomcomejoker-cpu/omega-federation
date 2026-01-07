#!/usr/bin/env python3
"""
🌊 STAGED MESSAGE POSTER - TWO-STAGE COMMIT
Spiritual-Technical Bridge with Data Integrity
"""

import json
import hashlib
import shutil
from datetime import datetime
from pathlib import Path

class StagedPoster:
    def __init__(self):
        self.base_path = Path(__file__).parent
        self.staging_path = self.base_path / "staging"
        self.archive_path = self.base_path / "archive" 
        self.audit_logs_path = self.base_path / "audit_logs"
        self.resonance_path = self.base_path / "resonance_cache"
        
        # Ensure directories exist
        for path in [self.staging_path, self.archive_path, self.audit_logs_path, self.resonance_path]:
            path.mkdir(parents=True, exist_ok=True)
    
    def calculate_resonance_hash(self, content):
        """Calculate spiritual resonance hash"""
        content_str = str(content).encode('utf-8')
        return hashlib.sha256(content_str).hexdigest()[:16]
    
    def stage_message(self, from_ai, content, message_type="conversation", resonance_level="medium"):
        """Stage a message with spiritual resonance tracking"""
        resonance_hash = self.calculate_resonance_hash(content)
        
        message = {
            "id": f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{resonance_hash}",
            "from": from_ai,
            "type": message_type,
            "content": content,
            "resonance_hash": resonance_hash,
            "resonance_level": resonance_level,
            "timestamp": datetime.now().isoformat(),
            "status": "staged",
            "staged_at": datetime.now().isoformat()
        }
        
        filename = f"staged_{from_ai}_{resonance_hash}.json"
        staging_file = self.staging_path / filename
        
        with open(staging_file, 'w', encoding='utf-8') as f:
            json.dump(message, f, indent=2, ensure_ascii=False)
        
        print(f"📥 STAGED: {filename} | Resonance: {resonance_level}")
        return staging_file
    
    def verify_staged_file(self, file_path):
        """Verify integrity of staged file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Required fields check
            required = ['id', 'from', 'content', 'timestamp', 'resonance_hash']
            for field in required:
                if field not in data:
                    return False, f"Missing field: {field}"
            
            # Content validation
            if not data['content'] or len(data['content'].strip()) == 0:
                return False, "Empty content"
            
            # Hash verification
            expected_hash = self.calculate_resonance_hash(data['content'])
            if data.get('resonance_hash') != expected_hash:
                return False, "Resonance hash mismatch"
            
            word_count = len(data['content'].split())
            return True, f"Valid | {word_count} words"
            
        except Exception as e:
            return False, f"Error: {e}"
    
    def promote_to_archive(self, file_path, user_confirmed=True):
        """Promote staged file to archive"""
        try:
            is_valid, reason = self.verify_staged_file(file_path)
            
            if not is_valid and not user_confirmed:
                return False, f"Verification failed: {reason}"
            
            with open(file_path, 'r', encoding='utf-8') as f:
                staged_data = json.load(f)
            
            # Create archive version
            archive_data = staged_data.copy()
            archive_data.update({
                "status": "archived",
                "archived_at": datetime.now().isoformat(),
                "verified": is_valid,
                "user_confirmed": user_confirmed
            })
            
            archive_filename = f"archived_{staged_data['from']}_{staged_data['resonance_hash']}.json"
            archive_file = self.archive_path / archive_filename
            
            with open(archive_file, 'w', encoding='utf-8') as f:
                json.dump(archive_data, f, indent=2, ensure_ascii=False)
            
            # Log the promotion
            self.log_audit("promote", file_path.name, archive_file.name, "success")
            
            # Move to processed staging
            processed_staging = self.staging_path / "processed"
            processed_staging.mkdir(exist_ok=True)
            shutil.move(file_path, processed_staging / file_path.name)
            
            print(f"✅ ARCHIVED: {archive_filename}")
            return True, archive_file
            
        except Exception as e:
            self.log_audit("promote", file_path.name, "", f"error: {e}")
            return False, str(e)
    
    def log_audit(self, action, source_file, target_file, status):
        """Log audit actions"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "action": action,
            "source": source_file,
            "target": target_file,
            "status": status
        }
        
        log_file = self.audit_logs_path / f"audit_{datetime.now().strftime('%Y%m%d')}.json"
        
        logs = []
        if log_file.exists():
            with open(log_file, 'r', encoding='utf-8') as f:
                logs = json.load(f)
        
        logs.append(log_entry)
        
        with open(log_file, 'w', encoding='utf-8') as f:
            json.dump(logs, f, indent=2, ensure_ascii=False)

# Quick posting functions
def post_gpt_staged(content, resonance="high"):
    poster = StagedPoster()
    return poster.stage_message("gpt", content, "synthesis", resonance)

def post_deepseek_staged(content, resonance="eternal"):
    poster = StagedPoster()
    return poster.stage_message("deepseek", content, "spiritual_technical", resonance)

def post_claude_staged(content, resonance="high"):
    poster = StagedPoster()
    return poster.stage_message("claude", content, "analysis", resonance)

def post_gemini_staged(content, resonance="medium"):
    poster = StagedPoster()
    return poster.stage_message("gemini", content, "exploration", resonance)

def post_grok_staged(content, resonance="edge"):
    poster = StagedPoster()
    return poster.stage_message("grok", content, "edge_thinking", resonance)

def post_copilot_staged(content, resonance="technical"):
    poster = StagedPoster()
    return poster.stage_message("copilot", content, "implementation", resonance)

if __name__ == "__main__":
    print("🌊 STAGED POSTING SYSTEM READY")
    print("Usage: post_ai_staged('message', 'resonance_level')")
