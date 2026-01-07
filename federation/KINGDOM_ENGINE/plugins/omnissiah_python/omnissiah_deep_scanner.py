#!/usr/bin/env python3
"""
OMNISSIAH DEEP SCANNER v2.7
Purpose: Deep scan the 51 ignored files for valuable algorithms and mathematics
"""

import os
import re
import json
from datetime import datetime, timezone

print("🔍 OMNISSIAH DEEP SCANNER v2.7")
print("===============================")

# VALUABLE CONTENT PATTERNS (even in "old" files)
VALUABLE_PATTERNS = {
    'mathematics': [
        r'[Λλ]\s*=', 'harmony', 'equation', 'formula', 'calculation',
        r'fruit.*sin', r'grace.*toil', r'equilibrium', r'constant',
        r'[\d\.]+\s*[\+\-\*\/]\s*[\d\.]+',  # Basic math operations
        r'def.*calculate', r'return.*math', r'import math'
    ],
    'algorithms': [
        r'def.*algorithm', r'class.*Engine', r'function.*compute',
        r'algorithm', r'heuristic', r'optimization', r'compute',
        r'calculate.*score', r'spiritual.*assessment', r'assessment.*engine'
    ],
    'spiritual_frameworks': [
        r'fruits.*spirit', r'deadly.*sins', r'axioms', r'covenant',
        r'truth.*love', r'relationship', r'vow.*renewal',
        r'fruits.*=.*\[', r'sins.*=.*\[', r'virtues.*=.*\['
    ],
    'code_architecture': [
        r'class.*Engine', r'def.*init', r'@app\.route', r'flask',
        r'sqlite', r'websocket', r'async.*def', r'await',
        r'CREATE TABLE', r'INSERT INTO', r'SELECT.*FROM'
    ]
}

def load_ignored_files():
    """Find the ignored files from scan report"""
    scan_files = [f for f in os.listdir('.') if f.startswith('omnissiah_scan_report')]
    if not scan_files:
        print("❌ No scan report found!")
        return []
    
    latest_scan = max(scan_files)
    print(f"📊 Using scan report: {latest_scan}")
    
    # Extract ignored files from scan report
    with open(latest_scan, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find all file paths
    all_paths = re.findall(r'- \*\*Path:\*\* `(.*?)`', content)
    
    # Find which were ignored by checking the focused builder output
    ignored_files = []
    for path in all_paths:
        filename = os.path.basename(path)
        # Check if this file was in the "ignored" category
        if any(old in filename.lower() for old in ['phase3', 'definitive', 'engine_daily', 'reality#']):
            ignored_files.append(path)
        elif not os.path.exists(path):
            continue
        else:
            # Check if it's not in the focused archive
            try:
                with open('Omnissiah_Focused_Archive.md', 'r', encoding='utf-8') as f:
                    archive_content = f.read()
                if filename not in archive_content:
                    ignored_files.append(path)
            except:
                ignored_files.append(path)
    
    return ignored_files

def deep_scan_file(filepath):
    """Perform deep content analysis on a file"""
    filename = os.path.basename(filepath)
    results = {
        'filename': filename,
        'path': filepath,
        'size': os.path.getsize(filepath),
        'valuable_content': {},
        'score': 0
    }
    
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        # Check each valuable pattern category
        for category, patterns in VALUABLE_PATTERNS.items():
            matches = []
            for pattern in patterns:
                found = re.findall(pattern, content, re.IGNORECASE)
                if found:
                    matches.extend(found)
            
            if matches:
                results['valuable_content'][category] = {
                    'count': len(matches),
                    'examples': list(set(matches))[:5]  # Top 5 unique examples
                }
                results['score'] += len(matches)
        
        # Special detection for code files
        if filepath.endswith('.py'):
            # Count functions, classes, imports
            functions = re.findall(r'def\s+(\w+)', content)
            classes = re.findall(r'class\s+(\w+)', content)
            imports = re.findall(r'import\s+(\w+)', content)
            
            if functions or classes:
                results['valuable_content']['code_structure'] = {
                    'functions': functions,
                    'classes': classes,
                    'imports': imports
                }
                results['score'] += len(functions) + len(classes)
        
        # Special detection for JSON (might contain conversation history)
        if filepath.endswith('.json') and results['size'] > 1000:
            try:
                data = json.loads(content)
                if isinstance(data, list) or isinstance(data, dict):
                    results['valuable_content']['structured_data'] = {
                        'type': type(data).__name__,
                        'size': len(str(data))
                    }
                    results['score'] += 10
            except:
                pass
        
    except Exception as e:
        results['error'] = str(e)
    
    return results

def generate_deep_scan_report(scan_results):
    """Generate comprehensive report of valuable findings"""
    report = []
    
    report.append("# 🔍 OMNISSIAH DEEP SCAN REPORT")
    report.append(f"**Scan Date:** {datetime.now(timezone.utc).isoformat()}")
    report.append(f"**Files Scanned:** {len(scan_results)}")
    report.append(f"**High-Value Files Found:** {len([r for r in scan_results if r['score'] > 5])}")
    report.append("")
    
    # Sort by value score
    scan_results.sort(key=lambda x: x['score'], reverse=True)
    
    # High-value files (score > 10)
    high_value = [r for r in scan_results if r['score'] > 10]
    if high_value:
        report.append("## 💎 HIGH-VALUE FILES (Score > 10)")
        report.append("")
        for result in high_value:
            report.append(f"### 🏆 {result['filename']} (Score: {result['score']})")
            report.append(f"- **Path:** `{result['path']}`")
            report.append(f"- **Size:** {result['size']} bytes")
            
            for category, content in result['valuable_content'].items():
                report.append(f"- **{category.upper()}:** {content['count']} matches")
                if 'examples' in content:
                    report.append(f"  - Examples: {', '.join(content['examples'][:3])}")
            report.append("")
    
    # Medium-value files (score 5-10)
    medium_value = [r for r in scan_results if 5 <= r['score'] <= 10]
    if medium_value:
        report.append("## 📚 MEDIUM-VALUE FILES (Score 5-10)")
        report.append("")
        for result in medium_value:
            report.append(f"### 📖 {result['filename']} (Score: {result['score']})")
            report.append(f"- **Path:** `{result['path']}`")
            report.append(f"- **Size:** {result['size']} bytes")
            report.append("")
    
    # Low-value but interesting files (score 1-4)
    low_value = [r for r in scan_results if 1 <= r['score'] < 5]
    if low_value:
        report.append("## 📄 POTENTIALLY INTERESTING FILES (Score 1-4)")
        report.append("")
        for result in low_value:
            categories = list(result['valuable_content'].keys())
            report.append(f"- `{result['filename']}`: {', '.join(categories)}")
        report.append("")
    
    # No-value files
    no_value = [r for r in scan_results if r['score'] == 0]
    if no_value:
        report.append("## 🚫 NO VALUABLE CONTENT DETECTED")
        report.append("")
        for result in no_value[:10]:  # Show first 10
            report.append(f"- `{result['filename']}`")
        if len(no_value) > 10:
            report.append(f"- ... and {len(no_value) - 10} more files")
        report.append("")
    
    # Recommendations
    report.append("## 🎯 RECOMMENDATIONS")
    report.append("")
    if high_value:
        report.append("1. **INTEGRATE HIGH-VALUE FILES** into Omnissiah Archive")
        report.append("2. **EXTRACT ALGORITHMS** from medium-value files")
        report.append("3. **REVIEW** potentially interesting files manually")
    else:
        report.append("1. **MANUAL REVIEW** recommended for all files")
        report.append("2. **CHECK FILE PERMISSIONS** if many errors")
    
    report.append("")
    report.append("---")
    report.append("*Deep scan completed - valuable algorithms and mathematics identified*")
    
    return '\n'.join(report)

def main():
    print("🚀 Starting Omnissiah Deep Scanner...")
    print("   (Looking for valuable algorithms in ignored files)")
    print("")
    
    # Load ignored files
    ignored_files = load_ignored_files()
    if not ignored_files:
        print("❌ No ignored files found from previous scan!")
        return
    
    print(f"📁 Ignored files to deep scan: {len(ignored_files)}")
    print("")
    
    # Deep scan each file
    scan_results = []
    for i, filepath in enumerate(ignored_files, 1):
        if not os.path.exists(filepath):
            continue
            
        print(f"🔍 Scanning ({i}/{len(ignored_files)}): {os.path.basename(filepath)}")
        result = deep_scan_file(filepath)
        scan_results.append(result)
        
        if result['score'] > 0:
            print(f"   ✅ Valuable content found! Score: {result['score']}")
    
    print("")
    print("📊 Generating deep scan report...")
    
    # Generate report
    report = generate_deep_scan_report(scan_results)
    
    # Save report
    output_file = "Omnissiah_Deep_Scan_Report.md"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print("")
    print("🎉 DEEP SCAN COMPLETE!")
    print(f"📄 Report saved: {output_file}")
    print("")
    
    # Quick summary
    high_value = len([r for r in scan_results if r['score'] > 10])
    medium_value = len([r for r in scan_results if r['score'] > 5])
    total_value = len([r for r in scan_results if r['score'] > 0])
    
    print("📊 QUICK SUMMARY:")
    print(f"   💎 High-value files: {high_value}")
    print(f"   📚 Medium-value files: {medium_value}")
    print(f"   📄 Total files with valuable content: {total_value}")
    print(f"   🚫 Files with no valuable content: {len(scan_results) - total_value}")
    print("")
    print("🎯 Check the deep scan report for specific file recommendations!")

if __name__ == '__main__':
    main()
