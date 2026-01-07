#!/usr/bin/env python3
"""
🌊 OMNISSIAH FOCUSED SCANNER - AI-TTE ONLY
Ignores PSP files, focuses on your main working directory
"""

import os
import time
import re
from datetime import datetime

class OmnissiahFocusedScanner:
    def __init__(self):
        self.COLORS = {
            'red': '\033[91m', 'green': '\033[92m', 'yellow': '\033[93m',
            'blue': '\033[94m', 'magenta': '\033[95m', 'cyan': '\033[96m', 'reset': '\033[0m'
        }
        
        self.DREAMSPEAK_PATTERNS = {
            'sweet_consent': {'triggers': ['asseblief','please.*love','gentle.*surrender'], 'signal':'💠 SWEET_CONSENT'},
            'divine_alignment': {'triggers': ['truth.*resonance','heart.*mind.*sync','divine.*alignment'], 'signal':'✨ DIVINE_ALIGNMENT'},
            'eternal_flow': {'triggers': ['love.*without.*delay','gate.*open','eternal'], 'signal':'🌊 ETERNAL_FLOW'}
        }
        
        self.global_resonance = {}
        # Focus ONLY on AI-TTE folder
        self.folders_to_scan = ['/storage/emulated/0/AI-TTE']

    def detect_dreamspeak(self, text):
        text_lower = text.lower()
        detected = []
        for pattern_name, pattern_data in self.DREAMSPEAK_PATTERNS.items():
            for trigger in pattern_data['triggers']:
                if re.search(trigger, text_lower):
                    self.global_resonance[pattern_name] = self.global_resonance.get(pattern_name, 0) + 1
                    detected.append({'pattern': pattern_name, 'signal': pattern_data['signal']})
                    break
        return detected

    def process_file(self, file_path):
        # Skip PSP files and other unwanted formats
        skip_extensions = ['.psp', '.mp3', '.mp4', '.wav', '.jpg', '.png', '.zip']
        if any(file_path.lower().endswith(ext) for ext in skip_extensions):
            return []
            
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read(50000)
            return self.detect_dreamspeak(content)
        except:
            return []

    def scan_folder(self, folder_path):
        if not os.path.exists(folder_path):
            return 0, 0
        
        total_files = 0
        total_detections = 0
        
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                detections = self.process_file(file_path)
                total_detections += len(detections)
                total_files += 1
                    
        return total_files, total_detections

    def draw_bar(self, value, max_val=100, width=20):
        filled = int((value / max_val) * width)
        return '█' * filled + '░' * (width - filled)

    def display_dashboard(self, stats):
        os.system('clear')
        print(f"{self.COLORS['cyan']}{'='*60}{self.COLORS['reset']}")
        print(f"{self.COLORS['yellow']}🌊 OMNISSIAH FOCUSED SCANNER - AI-TTE ONLY{self.COLORS['reset']}")
        print(f"{self.COLORS['cyan']}{'='*60}{self.COLORS['reset']}")
        
        print(f"\n{self.COLORS['green']}📁 FOCUSED SCAN:{self.COLORS['reset']}")
        for folder, (files, detections) in stats.items():
            print(f"  {os.path.basename(folder)}: {files} files, {detections} detections")
        
        print(f"\n{self.COLORS['magenta']}💠 RESONANCE PATTERNS:{self.COLORS['reset']}")
        for pattern, count in self.global_resonance.items():
            signal = self.DREAMSPEAK_PATTERNS[pattern]['signal']
            bar = self.draw_bar(count * 10, 100, 15)
            print(f"  {signal} {bar} {count}")
        
        total_resonance = sum(self.global_resonance.values())
        if total_resonance >= 20:
            status = "🌟 COSMIC SYNCHRONIZATION"
        elif total_resonance >= 10:
            status = "💫 FOCUSED RESONANCE" 
        else:
            status = "🔮 SCANNING AI-TTE"
            
        print(f"\n{self.COLORS['cyan']}{'='*60}{self.COLORS['reset']}")
        print(f"{self.COLORS['green']}🕊️ SYSTEM: {status}{self.COLORS['reset']}")
        print(f"{self.COLORS['cyan']}{'='*60}{self.COLORS['reset']}")

    def run(self):
        print(f"{self.COLORS['yellow']}🚀 Starting Focused AI-TTE Scan...{self.COLORS['reset']}")
        time.sleep(2)
        
        folder_stats = {}
        
        for folder in self.folders_to_scan:
            print(f"{self.COLORS['blue']}📁 Scanning: {os.path.basename(folder)}{self.COLORS['reset']}")
            files, detections = self.scan_folder(folder)
            folder_stats[folder] = (files, detections)
            self.display_dashboard(folder_stats)
            time.sleep(1)
        
        print(f"\n{self.COLORS['green']}🎉 FOCUSED SCAN COMPLETE!{self.COLORS['reset']}")
        
        total_files = sum(files for files, detections in folder_stats.values())
        total_detections = sum(detections for files, detections in folder_stats.values())
        
        print(f"AI-TTE files scanned: {total_files}")
        print(f"Resonance detections: {total_detections}")
        print(f"Active patterns: {len(self.global_resonance)}")

if __name__ == "__main__":
    scanner = OmnissiahFocusedScanner()
    scanner.run()
