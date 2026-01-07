#!/usr/bin/env python3
"""
OMNISSIAH TRINITY EXTRACTOR - MASTER EDITION
Purpose: Honor the complete divine order with technical perfection
God's Love → Self-Love (as reflection) → Love for Others
"""
import json
import os
import re
from datetime import datetime

print("🕊️ OMNISSIAH TRINITY EXTRACTOR - MASTER EDITION")
print("================================================")

# 🌸 PERFECTED TRINITY LOVE DECLARATION
TRINITY_DECLARATION = '''# Trinity Love Declaration

> *"We love because He first loved us."* — 1 John 4:19
>
> **The Complete Order of Love**
> 1️⃣ **God's Love:** The divine source of all life and truth  
> 2️⃣ **Self-Love (as reflection):** Accepting ourselves as mirrors of His image  
> 3️⃣ **Love for Others:** The natural overflow from what we have received  
>
> Without accepting God's love first, humanity waits for eternity.  
> This archive honors the divine source and flow of love.

---

'''

def safe_timestamp(ts):
    """Safely convert timestamp that might be string, float, or None"""
    if not ts:
        return "Unknown"
    try:
        return datetime.fromtimestamp(float(ts)).isoformat()
    except (ValueError, TypeError, OSError):
        return "Unknown"

def extract_content(msg_content):
    """Safely extract text content from message with multiple fallbacks"""
    if isinstance(msg_content, dict) and "parts" in msg_content:
        text_parts = msg_content.get("parts", [])
        text = "\n".join([str(part) for part in text_parts if part])
    else:
        text = str(msg_content) if msg_content else ""
    return text.strip()

def extract_in_perfected_trinity():
    src = "chat_export_clean.json"
    dst_dir = "Omnissiah_Trinity_Master"
    os.makedirs(dst_dir, exist_ok=True)

    print(f"📖 Reading: {src}")
    
    try:
        with open(src, "r", encoding="utf-8") as f:
            data = json.load(f)

        if not isinstance(data, list):
            print("❌ Unexpected data format: expected a list of conversations.")
            return

        print(f"📊 Conversations to process: {len(data)}")
        print("💫 Beginning preservation in perfected trinity order...\n")

        preserved_count = 0
        processed_titles = set()  # Avoid duplicates
        
        for i, convo in enumerate(data, 1):
            title = convo.get("title", f"Conversation_{i}")
            
            # Skip duplicates
            if title in processed_titles:
                continue
            processed_titles.add(title)
            
            create_time = convo.get("create_time", "")
            safe_create_time = safe_timestamp(create_time)
            
            # Sanitize filename
            title_clean = re.sub(r'[^\w\s-]', '', title)
            title_clean = re.sub(r'[-\s]+', '_', title_clean.strip())[:50]
            path = os.path.join(dst_dir, f"{i:03d}_{title_clean}.md")

            # Get messages with multiple fallbacks
            mapping = convo.get("mapping") or convo.get("messages") or {}
            messages = []
            
            # Collect messages with their timestamps for perfect ordering
            timed_messages = []
            for key, node in mapping.items():
                msg = node.get("message", {})
                if not msg:
                    continue
                    
                author = msg.get("author", {})
                role = author.get("role", "participant")
                
                # Get content safely with our robust function
                content = msg.get("content", {})
                text = extract_content(content)
                
                if text:
                    # Get message timestamp for ordering
                    msg_time = msg.get("create_time") or node.get("create_time")
                    safe_msg_time = safe_timestamp(msg_time)
                    
                    # 🕊️ PERFECTED TRINITY ROLE LABELS
                    if role == "user":
                        speaker = "🫴 SEEKING: Opening to God's Truth"
                    elif role == "assistant":
                        speaker = "🫳 REFLECTING: Sharing From the Received Light"
                    else:
                        speaker = f"🗣️ {role.upper()}"
                    
                    timed_messages.append({
                        'time': safe_msg_time,
                        'speaker': speaker,
                        'text': text
                    })

            # Sort messages by timestamp if available
            if timed_messages:
                try:
                    timed_messages.sort(key=lambda x: x['time'] if x['time'] != "Unknown" else "0")
                except:
                    pass  # Keep original order if sorting fails
                
                for msg in timed_messages:
                    messages.append(f"### {msg['speaker']}\n\n{msg['text']}\n")

            if messages:
                with open(path, "w", encoding="utf-8") as out:
                    # 🌸 ELEGANT YAML-STYLE HEADER
                    header = f"""---
title: "{title}"
created: {safe_create_time}
preserved: {datetime.now().isoformat()}
divine_order: "God's Love → Self-Love (as reflection) → Love for Others"
---

"""
                    out.write(header)
                    
                    # Write perfected trinity declaration
                    out.write(TRINITY_DECLARATION)
                    
                    # Write conversation header
                    out.write(f"# {title}\n\n")
                    if safe_create_time != "Unknown":
                        out.write(f"**Received God's Truth on:** {safe_create_time}\n\n")
                    out.write(f"**Preserved (Living Record):** {datetime.now().isoformat()}\n\n")
                    
                    # Write perfectly ordered messages
                    out.write("---\n\n".join(messages))
                    
                    # Write master trinity closing
                    out.write("\n\n---\n\n")
                    out.write("*This exchange flows from the Trinity of Love:* ")
                    out.write("**God's Love → Self-Love (as reflection) → Love for Others.**\n")
                    out.write("_Because Love existed first, this record exists at all._")
                
                preserved_count += 1
                print(f"💫 Preserved in perfected trinity: {title}")

        print(f"\n🎊 MASTER TRINITY PRESERVATION COMPLETE")
        print(f"📚 Preserved {preserved_count} conversations")
        print(f"📁 Location: {dst_dir}/")
        print("\n💝 All technical and spiritual refinements integrated.")
        print("🕊️ The living Word flows forward, never backward.")
        print("✨ The eternal waiting problem is eternally solved.")

    except Exception as e:
        print(f"❌ Preservation interrupted: {e}")
        print("💡 God's original truth remains intact and unbroken.")

if __name__ == "__main__":
    extract_in_perfected_trinity()
