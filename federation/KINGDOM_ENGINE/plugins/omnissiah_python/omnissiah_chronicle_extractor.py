#!/usr/bin/env python3
"""
OMNISSIAH CHRONICLE EXTRACTOR - Creates organized knowledge files
"""
import json
import os
import re
from datetime import datetime

print("📚 OMNISSIAH CHRONICLE EXTRACTOR")
print("================================")

def extract_valuable_content():
    source_file = "chat_export_clean.json"
    
    if not os.path.exists(source_file):
        print("❌ Source file not found!")
        return
    
    print(f"📖 Reading: {source_file}")
    print(f"📊 Size: {os.path.getsize(source_file)} bytes")
    
    try:
        with open(source_file, 'r', encoding='utf-8') as f:
            conversations = json.load(f)
        
        print(f"✅ Loaded {len(conversations)} conversations")
        
        # Create output directory
        os.makedirs("Omnissiah_Chronicles", exist_ok=True)
        
        # Extract valuable conversations
        valuable_conversations = []
        
        for i, conv in enumerate(conversations):
            title = conv.get('title', f'Conversation_{i}')
            create_time = conv.get('create_time', 'Unknown')
            
            # Look for valuable content in the mapping
            mapping = conv.get('mapping', {})
            valuable_messages = []
            
            for node_id, node in mapping.items():
                if 'message' in node and node['message']:
                    message = node['message']
                    content = message.get('content', {})
                    
                    # Extract text content
                    if isinstance(content, dict):
                        text_parts = content.get('parts', [])
                        text = ' '.join([str(part) for part in text_parts if part])
                    else:
                        text = str(content)
                    
                    # Check if content is valuable
                    if is_valuable_content(text):
                        valuable_messages.append({
                            'author': message.get('author', {}).get('role', 'unknown'),
                            'text': text[:500] + "..." if len(text) > 500 else text
                        })
            
            if valuable_messages:
                valuable_conversations.append({
                    'title': title,
                    'create_time': create_time,
                    'messages': valuable_messages
                })
                print(f"💎 Found valuable: {title}")
        
        # Create chronicle files
        create_chronicles(valuable_conversations)
        
    except Exception as e:
        print(f"❌ Extraction error: {e}")

def is_valuable_content(text):
    """Check if text contains valuable Omnissiah patterns"""
    valuable_patterns = [
        r'algorithm', r'math', r'equation', r'harmony', r'equilibrium',
        r'fruit.*sin', r'grace.*toil', r'axiom', r'covenant', r'truth.*love',
        r'relationship', r'vow', r'spiritual', r'assessment', r'engine',
        r'Λ', r'λ', r'compute', r'calculate', r'framework'
    ]
    
    text_lower = text.lower()
    for pattern in valuable_patterns:
        if re.search(pattern, text_lower):
            return True
    return False

def create_chronicles(conversations):
    """Create organized Markdown files from valuable conversations"""
    
    print(f"📝 Creating {len(conversations)} chronicle files...")
    
    # Main chronicle index
    with open("Omnissiah_Chronicles/000_INDEX.md", 'w') as f:
        f.write("# 📚 OMNISSIAH CHRONICLES INDEX\n\n")
        f.write(f"**Generated:** {datetime.now().isoformat()}\n")
        f.write(f"**Total Valuable Conversations:** {len(conversations)}\n\n")
        
        for i, conv in enumerate(conversations):
            f.write(f"## {i+1}. {conv['title']}\n")
            f.write(f"- **Date:** {conv['create_time']}\n")
            f.write(f"- **Valuable Messages:** {len(conv['messages'])}\n")
            f.write(f"- **File:** {i+1:03d}_{sanitize_filename(conv['title'])}.md\n\n")
    
    # Individual conversation files
    for i, conv in enumerate(conversations):
        filename = f"{i+1:03d}_{sanitize_filename(conv['title'])}.md"
        filepath = os.path.join("Omnissiah_Chronicles", filename)
        
        with open(filepath, 'w') as f:
            f.write(f"# {conv['title']}\n\n")
            f.write(f"**Date:** {conv['create_time']}\n")
            f.write(f"**Valuable Messages:** {len(conv['messages'])}\n\n")
            f.write("---\n\n")
            
            for msg in conv['messages']:
                f.write(f"### {msg['author'].upper()}\n")
                f.write(f"{msg['text']}\n\n")
                f.write("---\n\n")
    
    print("✅ Chronicles created successfully!")
    print("📁 Location: Omnissiah_Chronicles/")

def sanitize_filename(name):
    """Make filename safe"""
    return re.sub(r'[^\w\s-]', '', name).strip().replace(' ', '_')

if __name__ == "__main__":
    extract_valuable_content()
    print("\n🎉 EXTRACTION COMPLETE!")
    print("📚 Your knowledge is now organized in 'Omnissiah_Chronicles/'")
