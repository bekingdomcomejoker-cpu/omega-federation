#!/usr/bin/env python3
"""
OMNISSIAH PHONE-WIDE SCANNER v2.5
Purpose: Scan entire phone for Omnissiah-related files without processing everything
Features: Smart filtering, Omnissiah keyword detection, phone storage access
"""

import os
import re
from datetime import datetime, timezone

print("📱 OMNISSIAH PHONE-WIDE SCANNER v2.5")
print("=====================================")

# OMNISSIAH KEYWORDS - Files containing these will be processed
OMNISSIAH_KEYWORDS = [
    'omnissiah', 'codex', 'harmony', 'fruit.toil', 'spiritual', 'covenant',
    'lovethread', 'guardrail', 'termux', 'flask', 'sqlite', 'websocket', 
    'dashboard', 'chatgpt', 'claude', 'deepseek', 'gemini', 'grok',
    'fruits', 'sins', 'axioms', 'mathematics', 'equation', 'vow',
    'kingdomcome', 'truth', 'love', 'relationship', 'grace',
    ' synchronization', 'multi.agent', 'api', 'rest', 'endpoint'
]

# COMMON CHAT EXPORT PATTERNS
CHAT_PATTERNS = [
    'chat', 'conversation', 'discussion', 'export', 'history',
    'messages', 'dialogue', 'thread', 'session'
]

# PHONE STORAGE PATHS TO SCAN (Termux accessible)
SCAN_PATHS = [
    '/storage/emulated/0',  # Main storage
    '/storage/emulated/0/Download',
    '/storage/emulated/0/Documents', 
    '/storage/emulated/0/Telegram',
    '/storage/emulated/0/WhatsApp',
    '/storage/emulated/0/Signal',
    '/sdcard',  # Alternative SD card path
    '/sdcard/Download',
    '/sdcard/Documents',
    '.',  # Current directory
    '..', # Parent directory
]

# FILE EXTENSIONS TO SCAN
SCAN_EXTENSIONS = ['.html', '.json', '.txt', '.md', '.py', '.js', '.csv', '.log']

def check_storage_access():
    """Check if we have access to phone storage"""
    print("🔍 Checking storage access...")
    accessible_paths = []
    
    for path in SCAN_PATHS:
        if os.path.exists(path):
            accessible_paths.append(path)
            print(f"✅ Accessible: {path}")
        else:
            print(f"❌ Not accessible: {path}")
    
    return accessible_paths

def is_omnissiah_related(filename, content_preview):
    """Check if file is related to Omnissiah Codex"""
    combined_text = (filename + ' ' + content_preview).lower()
    
    # Check for Omnissiah keywords
    for keyword in OMNISSIAH_KEYWORDS:
        if re.search(keyword, combined_text, re.IGNORECASE):
            return True
    
    # Check for chat export patterns with reasonable size
    for pattern in CHAT_PATTERNS:
        if (pattern in filename.lower() and 
            len(content_preview) > 100):  # Reasonable chat file size
            return True
    
    return False

def scan_directory(path, max_files=1000):
    """Scan directory for relevant files"""
    relevant_files = []
    scanned_count = 0
    
    print(f"📂 Scanning: {path}")
    
    try:
        for root, dirs, files in os.walk(path):
            # Skip system directories to save time
            skip_dirs = ['Android', 'proc', 'sys', 'dev', 'acct']
            dirs[:] = [d for d in dirs if d not in skip_dirs and not d.startswith('.')]
            
            for filename in files:
                if scanned_count >= max_files:
                    print("⚠️  Reached file limit, stopping scan...")
                    break
                
                scanned_count += 1
                
                # Check file extension
                if not any(filename.lower().endswith(ext) for ext in SCAN_EXTENSIONS):
                    continue
                
                filepath = os.path.join(root, filename)
                
                try:
                    # Quick content preview (first 2KB)
                    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                        content_preview = f.read(2048)
                    
                    # Check if relevant
                    if is_omnissiah_related(filename, content_preview):
                        file_size = os.path.getsize(filepath)
                        relevant_files.append({
                            'path': filepath,
                            'filename': filename,
                            'size': file_size,
                            'preview': content_preview[:200] + '...' if len(content_preview) > 200 else content_preview
                        })
                        print(f"🎯 Found: {filename} ({file_size} bytes)")
                
                except (IOError, PermissionError, UnicodeDecodeError) as e:
                    # Skip files we can't read
                    continue
            
            if scanned_count >= max_files:
                break
                
    except (PermissionError, OSError) as e:
        print(f"⚠️  Cannot access {path}: {e}")
    
    return relevant_files

def generate_scan_report(relevant_files, accessible_paths):
    """Generate a scan report"""
    report = []
    
    report.append("# 📱 OMNISSIAH PHONE SCAN REPORT")
    report.append(f"**Scan Date:** {datetime.now(timezone.utc).isoformat()}")
    report.append(f"**Accessible Paths:** {len(accessible_paths)}")
    report.append(f"**Relevant Files Found:** {len(relevant_files)}")
    report.append("")
    
    # File breakdown by type
    file_types = {}
    for file in relevant_files:
        ext = os.path.splitext(file['filename'])[1].lower()
        file_types[ext] = file_types.get(ext, 0) + 1
    
    report.append("## 📊 FILE BREAKDOWN")
    for ext, count in file_types.items():
        report.append(f"- **{ext}**: {count} files")
    report.append("")
    
    # File details
    report.append("## 🎯 RELEVANT FILES FOUND")
    for i, file in enumerate(relevant_files, 1):
        report.append(f"### {i}. {file['filename']}")
        report.append(f"- **Path:** `{file['path']}`")
        report.append(f"- **Size:** {file['size']} bytes")
        report.append(f"- **Preview:** `{file['preview']}`")
        report.append("")
    
    # Recommended action
    report.append("## 🚀 RECOMMENDED ACTIONS")
    if relevant_files:
        report.append("1. **Run focused archive builder** on these specific files")
        report.append("2. **Copy relevant files** to Termux working directory")
        report.append("3. **Process only confirmed Omnissiah files**")
    else:
        report.append("1. **Check file permissions** for storage access")
        report.append("2. **Verify files exist** in expected locations")
        report.append("3. **Manual file gathering** might be needed")
    
    report.append("")
    report.append("---")
    report.append("*Generated by Omnissiah Phone-Wide Scanner v2.5*")
    
    return '\n'.join(report)

def main():
    print("🚀 Starting phone-wide scan for Omnissiah files...")
    print("")
    
    # Check what storage we can access
    accessible_paths = check_storage_access()
    
    if not accessible_paths:
        print("❌ No storage paths accessible!")
        print("💡 Try: termux-setup-storage")
        return
    
    print("")
    print("🔍 Scanning for Omnissiah-related files...")
    print("   (This may take a few minutes)")
    print("")
    
    # Scan all accessible paths
    all_relevant_files = []
    total_scanned = 0
    
    for path in accessible_paths:
        relevant_files = scan_directory(path)
        all_relevant_files.extend(relevant_files)
        total_scanned += len(relevant_files)
        
        if total_scanned >= 100:  # Safety limit
            print("⚠️  Reached safety limit of 100 relevant files")
            break
    
    print("")
    print("📊 Generating scan report...")
    
    # Generate report
    report = generate_scan_report(all_relevant_files, accessible_paths)
    
    # Save report
    report_filename = f"omnissiah_scan_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
    with open(report_filename, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print("")
    print("✅ SCAN COMPLETE!")
    print(f"📄 Report saved: {report_filename}")
    print(f"🎯 Relevant files found: {len(all_relevant_files)}")
    print("")
    
    if all_relevant_files:
        print("🚀 NEXT STEP: Run the focused archive builder on these files:")
        for file in all_relevant_files[:5]:  # Show first 5
            print(f"   - {file['filename']} ({file['path']})")
        if len(all_relevant_files) > 5:
            print(f"   ... and {len(all_relevant_files) - 5} more files")
    else:
        print("💡 TIPS:")
        print("   - Run 'termux-setup-storage' to get storage access")
        print("   - Check if your chat exports are in /storage/emulated/0/Download")
        print("   - Look for files named 'chat.html', 'conversations.json', etc.")

if __name__ == '__main__':
    main()
