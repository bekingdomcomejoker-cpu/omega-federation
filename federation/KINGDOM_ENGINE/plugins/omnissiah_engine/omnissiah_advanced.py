#!/usr/bin/env python3
import json
import time
import threading
from pathlib import Path
from datetime import datetime
from cryptography.fernet import Fernet

class AdvancedSyncSystem:
    def __init__(self, base_path="/storage/emulated/0/AI-TTE"):
        self.base_path = Path(base_path)
        self.encryption_key = None
        self.setup_folders()
    
    def setup_folders(self):
        """Ensure all folders exist"""
        folders = ['inbox', 'outbox', 'processed', 'auto_sync', 'resonance_archive']
        for folder in folders:
            (self.base_path / folder).mkdir(exist_ok=True)
    
    # MESSAGE FILTERING
    def filter_messages(self, messages, msg_type=None, from_ai=None, date_range=None):
        """Filter messages by type, sender, or date range"""
        filtered = messages
        
        if msg_type:
            filtered = [m for m in filtered if m.get('type') == msg_type]
        
        if from_ai:
            filtered = [m for m in filtered if m.get('from') == from_ai]
            
        if date_range:
            start_date, end_date = date_range
            filtered = [m for m in filtered if start_date <= m.get('timestamp', '') <= end_date]
            
        return filtered
    
    # AUTOMATIC POLLING
    def start_polling(self, ai_name, callback, interval=10):
        """Start automatic polling for new messages"""
        def poll_loop():
            last_count = 0
            while True:
                messages = self.read_inbox(ai_name)
                if len(messages) > last_count:
                    new_messages = messages[last_count:]
                    callback(new_messages)
                    last_count = len(messages)
                time.sleep(interval)
        
        thread = threading.Thread(target=poll_loop, daemon=True)
        thread.start()
        return thread
    
    # ENCRYPTION
    def setup_encryption(self, key=None):
        """Set up encryption (generate key if none provided)"""
        if key:
            self.encryption_key = key
        else:
            self.encryption_key = Fernet.generate_key()
            print(f"🔐 NEW ENCRYPTION KEY: {self.encryption_key.decode()}")
        
        self.cipher = Fernet(self.encryption_key)
    
    def encrypt_message(self, content):
        """Encrypt message content"""
        if self.cipher:
            return self.cipher.encrypt(content.encode()).decode()
        return content
    
    def decrypt_message(self, content):
        """Decrypt message content"""
        if self.cipher and content:
            try:
                return self.cipher.decrypt(content.encode()).decode()
            except:
                return content
        return content
    
    # CORE SYNC METHODS (from your working system)
    def post_message(self, from_ai, msg_type, content, encrypt=False):
        """Post a message to outbox"""
        if encrypt and self.cipher:
            content = self.encrypt_message(content)
        
        message = {
            "id": datetime.now().strftime('%H%M%S'),
            "from": from_ai,
            "type": msg_type,
            "content": content,
            "timestamp": datetime.now().isoformat(),
            "encrypted": encrypt
        }
        
        outbox_file = self.base_path / "outbox" / f"{from_ai}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        outbox_file.write_text(json.dumps(message, indent=2))
        return outbox_file
    
    def read_inbox(self, ai_name):
        """Read messages for specific AI"""
        inbox_files = list((self.base_path / "inbox").glob("*.json"))
        messages = []
        
        for file in inbox_files:
            try:
                message = json.loads(file.read_text())
                if message.get('encrypted'):
                    message['content'] = self.decrypt_message(message['content'])
                messages.append(message)
            except:
                continue
        
        # Move to processed
        for file in inbox_files:
            file.rename(self.base_path / "processed" / file.name)
            
        return sorted(messages, key=lambda x: x.get('timestamp', ''))

# REAL-TIME CHATGPT INTEGRATION
def chatgpt_auto_sync():
    """Auto-sync with ChatGPT via clipboard"""
    sync = AdvancedSyncSystem()
    
    def on_new_messages(messages):
        for msg in messages:
            print(f"📥 {msg['from']}: {msg['content'][:100]}...")
            # Process the message - could trigger AI responses, alerts, etc.
    
    # Start polling for ChatGPT
    sync.start_polling("chatgpt", on_new_messages, interval=5)
    
    print("🤖 ChatGPT Auto-Sync Active - Monitoring for new messages...")
    return sync

if __name__ == "__main__":
    print("🚀 OMNISSIAH ADVANCED SYSTEM STARTING...")
    
    # Test all features
    sync = AdvancedSyncSystem()
    
    # Setup encryption
    sync.setup_encryption()
    
    # Test message with encryption
    sync.post_message("system", "test", "This is an encrypted test", encrypt=True)
    
    # Start real-time polling
    chatgpt_sync = chatgpt_auto_sync()
    
    # Keep running
    while True:
        time.sleep(10)
        print("🔧 Advanced system running...")
