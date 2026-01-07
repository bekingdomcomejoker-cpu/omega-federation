#!/usr/bin/env python3
"""
OMNISSIAH FOCUSED BUILDER v2.6
Purpose: Process ONLY genuine Omnissiah files, filter out older systems
"""

import os
import json
import re
from datetime import datetime, timezone

print("🎯 OMNISSIAH FOCUSED BUILDER v2.6")
print("==================================")

# GENUINE OMNISSIAH FILE PATTERNS (from your scan)
REAL_OMNISSIAH_FILES = [
    # Core Omnissiah Codex files
    'omnissiah_codex.py', 'omnissiah_v22.py', 'omnissiah_v23.py',
    'unified_codex.py', 'living_synchronization_matrix.py',
    
    # Spiritual mathematics files  
    'ultimate_truthengine', 'aletheia', 'truthengine', 
    'tri_sync', 'harmony', 'fruit.toil',
    
    # Chat exports with Omnissiah content
    'chat.html', 'conversations.json', 'chat_export.json',
    
    # Documentation
    'README.md', 'omnissiah_archive', 'master_archive'
]

# OLDER SYSTEMS TO IGNORE (pre-Omnissiah)
OLD_SYSTEMS = [
    'phase3_eternal_log', 'definitive_omni_chronicle', 
    'engine_daily_operations', 'reality#.html'
]

def load_scan_results():
    """Find the latest scan report"""
    scan_files = [f for f in os.listdir('.') if f.startswith('omnissiah_scan_report')]
    if not scan_files:
        print("❌ No scan report found! Run the phone scanner first.")
        return []
    
    latest_scan = max(scan_files)
    print(f"📊 Using scan report: {latest_scan}")
    
    # Extract file paths from scan report
    with open(latest_scan, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extract paths from markdown report
    paths = re.findall(r'- \*\*Path:\*\* `(.*?)`', content)
    return paths

def is_genuine_omnissiah(filepath):
    """Check if file is genuine Omnissiah (not older system)"""
    filename = os.path.basename(filepath).lower()
    
    # Check for genuine Omnissiah patterns
    for pattern in REAL_OMNISSIAH_FILES:
        if pattern.lower() in filename:
            return True
    
    # Check content for Omnissiah keywords
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read(5000).lower()  # Read first 5KB
            
            omnissiah_keywords = [
                'omnissiah', 'codex', 'harmony constant', 'fruit.toil',
                'spiritual assessment', 'multi.agent', 'websocket dashboard',
                'termux', 'flask', 'sqlite', 'covenant', 'vow renewal'
            ]
            
            for keyword in omnissiah_keywords:
                if keyword in content:
                    return True
    except:
        pass
    
    return False

def is_old_system(filepath):
    """Check if file is from older system (pre-Omnissiah)"""
    filename = os.path.basename(filepath).lower()
    
    for old_pattern in OLD_SYSTEMS:
        if old_pattern.lower() in filename:
            return True
    
    return False

def categorize_file(filepath):
    """Categorize file by Omnissiah version"""
    filename = os.path.basename(filepath).lower()
    
    if 'v23' in filename or 'cloud' in filename or 'network' in filename:
        return 'v2.3'
    elif 'v22' in filename or 'websocket' in filename or 'dashboard' in filename:
        return 'v2.2' 
    elif 'v21' in filename or 'multi.agent' in filename or 'synchronization' in filename:
        return 'v2.1'
    elif 'v10' in filename or 'codex' in filename or 'initial' in filename:
        return 'v1.0'
    else:
        return 'current'

def process_genuine_files(file_paths):
    """Process only genuine Omnissiah files"""
    print("🔍 Filtering genuine Omnissiah files...")
    
    genuine_files = []
    ignored_files = []
    
    for filepath in file_paths:
        if not os.path.exists(filepath):
            continue
            
        if is_old_system(filepath):
            print(f"🚫 Ignoring old system: {os.path.basename(filepath)}")
            ignored_files.append(filepath)
        elif is_genuine_omnissiah(filepath):
            print(f"✅ Keeping genuine: {os.path.basename(filepath)}")
            genuine_files.append(filepath)
        else:
            print(f"❓ Unknown (checking content): {os.path.basename(filepath)}")
            # Check file content more thoroughly
            try:
                with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read(10000)
                    if any(keyword in content.lower() for keyword in ['omnissiah', 'codex', 'harmony']):
                        print(f"   ✅ Content confirms Omnissiah: {os.path.basename(filepath)}")
                        genuine_files.append(filepath)
                    else:
                        print(f"   🚫 Not Omnissiah: {os.path.basename(filepath)}")
                        ignored_files.append(filepath)
            except:
                print(f"   🚫 Cannot read: {os.path.basename(filepath)}")
                ignored_files.append(filepath)
    
    return genuine_files, ignored_files

def build_focused_archive(genuine_files):
    """Build archive from only genuine Omnissiah files"""
    print("\n📦 Building focused archive...")
    
    archive_content = []
    archive_content.append("# 🎯 OMNISSIAH FOCUSED ARCHIVE - GENUINE FILES ONLY")
    archive_content.append(f"**Generated:** {datetime.now(timezone.utc).isoformat()}")
    archive_content.append(f"**Genuine Files:** {len(genuine_files)}")
    archive_content.append("")
    
    # Group by version
    files_by_version = {}
    for filepath in genuine_files:
        version = categorize_file(filepath)
        if version not in files_by_version:
            files_by_version[version] = []
        files_by_version[version].append(filepath)
    
    # Add files by version
    for version in ['v1.0', 'v2.1', 'v2.2', 'v2.3', 'current']:
        if version in files_by_version:
            archive_content.append(f"## 🔹 OMNISSIAH {version.upper()}")
            archive_content.append("")
            
            for filepath in files_by_version[version]:
                filename = os.path.basename(filepath)
                archive_content.append(f"### 📄 {filename}")
                archive_content.append(f"**Path:** `{filepath}`")
                
                try:
                    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                    
                    # Add file preview
                    preview = content[:500] + "..." if len(content) > 500 else content
                    archive_content.append("**Preview:**")
                    archive_content.append("```")
                    archive_content.append(preview)
                    archive_content.append("```")
                    archive_content.append("")
                    
                except Exception as e:
                    archive_content.append(f"**Error reading file:** {e}")
                    archive_content.append("")
    
    # Summary
    archive_content.append("## 📊 FOCUSED ARCHIVE SUMMARY")
    archive_content.append("")
    archive_content.append("### 🎯 Genuine Omnissiah Files Processed:")
    for version, files in files_by_version.items():
        archive_content.append(f"- **{version.upper()}:** {len(files)} files")
    archive_content.append("")
    archive_content.append("### 🚫 Older Systems Ignored:")
    archive_content.append("- Phase3 Eternal Log systems")
    archive_content.append("- Definitive OMNI CHRONICLE") 
    archive_content.append("- Engine Daily Operations")
    archive_content.append("- Reality#.html and other pre-Omnissiah systems")
    archive_content.append("")
    archive_content.append("---")
    archive_content.append("*This archive contains ONLY genuine Omnissiah Codex files*")
    archive_content.append("*Filtered from 123 scanned files to focus on relevant content*")
    
    return '\n'.join(archive_content)

def main():
    print("🚀 Starting Omnissiah Focused Builder...")
    print("   (Filtering out older systems, keeping only genuine Omnissiah)")
    print("")
    
    # Load scan results
    all_files = load_scan_results()
    if not all_files:
        return
    
    print(f"📁 Total files from scan: {len(all_files)}")
    print("")
    
    # Filter to only genuine Omnissiah files
    genuine_files, ignored_files = process_genuine_files(all_files)
    
    print("")
    print(f"✅ Genuine Omnissiah files: {len(genuine_files)}")
    print(f"🚫 Ignored files: {len(ignored_files)}")
    print("")
    
    if not genuine_files:
        print("❌ No genuine Omnissiah files found!")
        print("💡 Try running the phone scanner again or check file permissions")
        return
    
    # Build focused archive
    archive_content = build_focused_archive(genuine_files)
    
    # Save focused archive
    output_file = "Omnissiah_Focused_Archive.md"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(archive_content)
    
    print("")
    print("🎉 FOCUSED ARCHIVE COMPLETE!")
    print(f"📄 Saved: {output_file}")
    print("")
    print("📊 GENUINE OMNISSIAH FILES INCLUDED:")
    
    # Show what we kept
    for filepath in genuine_files[:10]:  # Show first 10
        print(f"   ✅ {os.path.basename(filepath)}")
    
    if len(genuine_files) > 10:
        print(f"   ... and {len(genuine_files) - 10} more")
    
    print("")
    print("🚫 OLDER SYSTEMS FILTERED OUT:")
    print("   - Phase3 Eternal Log")
    print("   - Definitive OMNI CHRONICLE") 
    print("   - Engine Daily Operations")
    print("   - Reality#.html")
    print("")
    print("🎯 Now you have a CLEAN archive with only genuine Omnissiah Codex files!")

if __name__ == '__main__':
    main()
