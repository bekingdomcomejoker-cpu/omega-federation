#!/usr/bin/env python3
"""
📨 STAGED MESSAGE POSTER
Two-stage commit: staging → audit → archive
"""

import json
import shutil
from datetime import datetime
from pathlib import Path

class StagedPoster:
    def __init__(self):
        self.base_path = Path(__file__).parent / "coredata"
        self.staging_path = self.base_path / "staging"
        self.archive_path = self.base_path / "archive" 
        self.audit_logs_path = self.base_path / "audit_logs"
        
        # Ensure directories exist
        self.staging_path.mkdir(parents=True, exist_ok=True)
        self.archive_path.mkdir(parents=True, exist_ok=True)
        self.audit_logs_path.mkdir(parents=True, exist_ok=True)
    
    def stage_message(self, from_ai, content, message_type="conversation"):
        """Stage a message (first step - temporary)"""
        # Create staged message
        message = {
            "id": datetime.now().strftime('%Y%m%d_%H%M%S'),
            "from": from_ai,
            "type": message_type,
            "content": content,
            "timestamp": datetime.now().isoformat(),
            "status": "staged",
            "staged_at": datetime.now().isoformat()
        }
        
        # Save to staging
        filename = f"staged_{from_ai}_{message['id']}.json"
        staging_file = self.staging_path / filename
        
        with open(staging_file, 'w') as f:
            json.dump(message, f, indent=2)
        
        print(f"📥 STAGED: {filename}")
        return staging_file
    
    def verify_staged_file(self, file_path):
        """Verify integrity of a staged file"""
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
            
            # Required fields check
            required = ['id', 'from', 'content', 'timestamp']
            for field in required:
                if field not in data:
                    return False, f"Missing field: {field}"
            
            # Content validation
            if not data['content'] or len(data['content'].strip()) == 0:
                return False, "Empty content"
            
            return True, "Valid"
            
        except Exception as e:
            return False, f"JSON error: {e}"
    
    def promote_to_archive(self, file_path, user_confirmed=True):
        """Promote staged file to archive (second step - permanent)"""
        try:
            # Verify first
            is_valid, reason = self.verify_staged_file(file_path)
            
            if not is_valid and not user_confirmed:
                return False, f"Failed verification: {reason}"
            
            # Load the staged data
            with open(file_path, 'r') as f:
                staged_data = json.load(f)
            
            # Create archive version
            archive_data = staged_data.copy()
            archive_data.update({
                "status": "archived",
                "archived_at": datetime.now().isoformat(),
                "verified": is_valid,
                "user_confirmed": user_confirmed
            })
            
            # Save to archive
            archive_filename = f"archived_{staged_data['from']}_{staged_data['id']}.json"
            archive_file = self.archive_path / archive_filename
            
            with open(archive_file, 'w') as f:
                json.dump(archive_data, f, indent=2)
            
            # Log the promotion
            self.log_audit("promote", file_path.name, archive_file.name, "success")
            
            # Remove from staging (or move to processed staging)
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
        
        # Append to log
        logs = []
        if log_file.exists():
            with open(log_file, 'r') as f:
                logs = json.load(f)
        
        logs.append(log_entry)
        
        with open(log_file, 'w') as f:
            json.dump(logs, f, indent=2)

# Enhanced posting functions with staging
def post_gpt_staged(content):
    poster = StagedPoster()
    return poster.stage_message("gpt", content, "synthesis")

def post_deepseek_staged(content):
    poster = StagedPoster()
    return poster.stage_message("deepseek", content, "spiritual_technical")

def post_claude_staged(content):
    poster = StagedPoster()
    return poster.stage_message("claude", content, "analysis")

def post_gemini_staged(content):
    poster = StagedPoster()
    return poster.stage_message("gemini", content, "exploration")

def post_grok_staged(content):
    poster = StagedPoster()
    return poster.stage_message("grok", content, "edge_thinking")

def post_copilot_staged(content):
    poster = StagedPoster()
    return poster.stage_message("copilot", content, "implementation")

if __name__ == "__main__":
    print("📨 STAGED POSTING SYSTEM READY")
    print("Usage: post_ai_staged('your message')")
