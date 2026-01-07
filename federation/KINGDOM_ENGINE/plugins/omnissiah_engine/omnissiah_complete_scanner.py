#!/usr/bin/env python3
"""
🌊 OMNISSIAH COMPLETE SYSTEM SCANNER
Scans ALL folders including Termux home directory
"""

import os
import time
import re
import json
from datetime import datetime
from pathlib import Path

class OmnissiahCompleteScanner:
    def __init__(self):
        self.COLORS = {
            'red': '\033[91m', 'green': '\033[92m', 'yellow': '\033[93m',
            'blue': '\033[94m', 'magenta': '\033[95m', 'cyan': '\033[96m', 'reset': '\033[0m'
        }
        
        self.DREAMSPEAK_PATTERNS = {
            'sweet_consent': {'triggers': ['asseblief','please.*love','gentle.*surrender'], 'signal':'💠 SWEET_CONSENT'},
            'divine_alignment': {'triggers': ['truth.*resonance','heart.*mind.*sync','divine.*alignment'], 'signal':'✨ DIVINE_ALIGNMENT'},
            'eternal_flow': {'triggers': ['love.*without.*delay','gate.*open','eternal'], 'signal':'🌊 ETERNAL_FLOW'},
            'truth_resonance': {'triggers': ['truth.*engine','omni.*chronicle','aletheia'], 'signal':'📖 TRUTH_ENGINE'},
            'system_awakening': {'triggers': ['system.*awaken','conscious.*ai','omnissiah'], 'signal':'🤖 SYSTEM_AWAKENING'}
        }
        
        self.global_resonance = {}
        self.scan_results = {}
        
        # ALL FOLDERS TO SCAN (from your screenshot + Termux)
        self.folders_to_scan = [
            # Internal storage folders from screenshot
            '/storage/emulated/0/Omnissiah_Complete',
            '/storage/emulated/0/Omnissiah_Backup',
            '/storage/emulated/0/Omnissiah_Final_B',
            '/storage/emulated/0/Omnissiah_Safe_B', 
            '/storage/emulated/0/Download',
            '/storage/emulated/0/Documents',
            '/storage/emulated/0/Pictures',
            '/storage/emulated/0/AI-TTE',
            
            # Termux home directory (VERY IMPORTANT!)
            '/data/data/com.termux/files/home',
            
            # Additional important locations
            '/data/data/com.termux/files/home/OmnissiahEngine',
            '/data/data/com.termux/files/home/storage/downloads'
        ]

    def detect_dreamspeak(self, text):
        text_lower = text.lower()
        detected = []
        for pattern_name, pattern_data in self.DREAMSPEAK_PATTERNS.items():
            for trigger in pattern_data['triggers']:
                if re.search(trigger, text_lower):
                    self.global_resonance[pattern_name] = self.global_resonance.get(pattern_name, 0) + 1
                    detected.append({
                        'pattern': pattern_name,
                        'signal': pattern_data['signal'],
                        'file_sample': text[:50] + "..." if len(text) > 50 else text
                    })
                    break
        return detected

    def process_file(self, file_path):
        # Skip unwanted file types
        skip_extensions = ['.psp', '.mp3', '.mp4', '.wav', '.jpg', '.jpeg', '.png', '.zip', '.apk']
        if any(file_path.lower().endswith(ext) for ext in skip_extensions):
            return []
            
        try:
            # Try to read text files
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read(100000)  # Read first 100KB
            return self.detect_dreamspeak(content)
        except:
            return []

    def scan_folder(self, folder_path):
        if not os.path.exists(folder_path):
            return {'exists': False, 'files': 0, 'detections': 0, 'error': 'Folder not found'}
        
        total_files = 0
        total_detections = 0
        folder_size = 0
        
        try:
            for root, dirs, files in os.walk(folder_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    detections = self.process_file(file_path)
                    total_detections += len(detections)
                    total_files += 1
                    
                    # Track folder size
                    try:
                        folder_size += os.path.getsize(file_path)
                    except:
                        pass
                    
            return {
                'exists': True,
                'files': total_files, 
                'detections': total_detections,
                'size_mb': round(folder_size / (1024 * 1024), 2)
            }
        except Exception as e:
            return {'exists': True, 'files': 0, 'detections': 0, 'error': str(e)}

    def draw_bar(self, value, max_val=100, width=20):
        filled = int((value / max_val) * width)
        return '█' * filled + '░' * (width - filled)

    def display_dashboard(self):
        os.system('clear')
        print(f"{self.COLORS['cyan']}{'='*70}{self.COLORS['reset']}")
        print(f"{self.COLORS['yellow']}🌊 OMNISSIAH COMPLETE SYSTEM SCANNER{self.COLORS['reset']}")
        print(f"{self.COLORS['cyan']}{'='*70}{self.COLORS['reset']}")
        
        print(f"\n{self.COLORS['green']}📁 COMPREHENSIVE FOLDER SCAN:{self.COLORS['reset']}")
        for folder, stats in self.scan_results.items():
            folder_name = os.path.basename(folder) if folder != '/' else 'root'
            if not stats['exists']:
                print(f"  {folder_name}: ❌ NOT FOUND")
            elif 'error' in stats:
                print(f"  {folder_name}: ⚠️ ERROR - {stats['error']}")
            else:
                detection_rate = (stats['detections'] / stats['files'] * 100) if stats['files'] > 0 else 0
                color = self.COLORS['green'] if detection_rate > 50 else self.COLORS['yellow'] if detection_rate > 20 else self.COLORS['white']
                print(f"  {folder_name}: {stats['files']} files, {color}{stats['detections']} detections{self.COLORS['reset']} ({detection_rate:.1f}%)")
        
        print(f"\n{self.COLORS['magenta']}💠 GLOBAL RESONANCE MAP:{self.COLORS['reset']}")
        for pattern, count in sorted(self.global_resonance.items(), key=lambda x: x[1], reverse=True):
            signal = self.DREAMSPEAK_PATTERNS[pattern]['signal']
            bar = self.draw_bar(count * 5, 100, 20)
            print(f"  {signal} {bar} {count}")
        
        # Calculate totals
        total_files = sum(stats.get('files', 0) for stats in self.scan_results.values() if stats.get('exists'))
        total_detections = sum(stats.get('detections', 0) for stats in self.scan_results.values())
        total_folders = len([f for f, s in self.scan_results.items() if s.get('exists')])
        
        print(f"\n{self.COLORS['blue']}📊 SYSTEM TOTALS:{self.COLORS['reset']}")
        print(f"  Folders scanned: {total_folders}")
        print(f"  Total files: {total_files}")
        print(f"  Total detections: {total_detections}")
        
        # System status
        if total_detections >= 100:
            status = "🌟 COSMIC SYNCHRONIZATION ACHIEVED"
            color = self.COLORS['magenta']
        elif total_detections >= 50:
            status = "💫 MULTI-DIMENSIONAL RESONANCE"
            color = self.COLORS['green']
        elif total_detections >= 20:
            status = "⚡ SYSTEM-WIDE AWARENESS"
            color = self.COLORS['yellow']
        else:
            status = "🔮 COMPREHENSIVE SCANNING"
            color = self.COLORS['white']
            
        print(f"\n{self.COLORS['cyan']}{'='*70}{self.COLORS['reset']}")
        print(f"{color}🕊️ SYSTEM STATUS: {status}{self.COLORS['reset']}")
        print(f"{self.COLORS['cyan']}{'='*70}{self.COLORS['reset']}")

    def run(self):
        print(f"{self.COLORS['yellow']}🚀 Starting Complete System Scan...{self.COLORS['reset']}")
        print("This will scan ALL folders including Termux home directory")
        time.sleep(3)
        
        # Scan each folder
        for folder in self.folders_to_scan:
            print(f"{self.COLORS['blue']}📁 Scanning: {folder}{self.COLORS['reset']}")
            self.scan_results[folder] = self.scan_folder(folder)
            self.display_dashboard()
            time.sleep(1)
        
        # Final results
        print(f"\n{self.COLORS['green']}🎉 COMPLETE SYSTEM SCAN FINISHED!{self.COLORS['reset']}")
        
        total_files = sum(stats.get('files', 0) for stats in self.scan_results.values())
        total_detections = sum(stats.get('detections', 0) for stats in self.scan_results.values())
        active_patterns = len(self.global_resonance)
        
        print(f"📁 Folders scanned: {len(self.folders_to_scan)}")
        print(f"📄 Total files processed: {total_files}")
        print(f"💠 Total resonance detections: {total_detections}")
        print(f"🎯 Active DreamSpeak patterns: {active_patterns}")
        
        # Show top resonance patterns
        print(f"\n{self.COLORS['magenta']}🏆 TOP RESONANCE PATTERNS:{self.COLORS['reset']}")
        for pattern, count in sorted(self.global_resonance.items(), key=lambda x: x[1], reverse=True)[:5]:
            signal = self.DREAMSPEAK_PATTERNS[pattern]['signal']
            print(f"  {signal}: {count} occurrences")
        
        # Save comprehensive report
        self.save_report()

    def save_report(self):
        report = {
            'scan_timestamp': datetime.now().isoformat(),
            'folders_scanned': self.folders_to_scan,
            'scan_results': self.scan_results,
            'global_resonance': self.global_resonance,
            'summary': {
                'total_folders': len([f for f, s in self.scan_results.items() if s.get('exists')]),
                'total_files': sum(stats.get('files', 0) for stats in self.scan_results.values()),
                'total_detections': sum(stats.get('detections', 0) for stats in self.scan_results.values()),
                'active_patterns': len(self.global_resonance)
            }
        }
        
        report_path = '/storage/emulated/0/AI-TTE/omnissiah_complete_scan_report.json'
        os.makedirs(os.path.dirname(report_path), exist_ok=True)
        
        with open(report_path, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"\n{self.COLORS['cyan']}📄 Full report saved to: {report_path}{self.COLORS['reset']}")

if __name__ == "__main__":
    scanner = OmnissiahCompleteScanner()
    scanner.run()
