
#!/usr/bin/env python3
import json
import os
import re
from datetime import datetime

def extract_omnissiah_knowledge():
    print("🏆 OMNISSIAH KNOWLEDGE EXTRACTOR")
    print("================================")
    
    # Try the clean export first
    files_to_try = [
        "chat_export_clean.json",
        "chat_export.json", 
        "sample_chat_export.json"
    ]
    
    for file in files_to_try:
        if os.path.exists(file):
            print(f"🎯 Found: {file} ({os.path.getsize(file)} bytes)")
            return file
    return None

if __name__ == "__main__":
    source_file = extract_omnissiah_knowledge()
    if source_file:
        print(f"🚀 Ready to extract knowledge from: {source_file}")
        print("💡 Next: We'll parse the JSON and create organized .md files")
    else:
        print("❌ No source files found")
