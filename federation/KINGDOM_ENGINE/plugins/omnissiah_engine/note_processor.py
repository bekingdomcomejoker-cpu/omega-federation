#!/usr/bin/env python3
"""
📝 OMNISSIAH NOTE PROCESSOR
For copy-pasting notes that can't be accessed directly
"""

import re
import json
from datetime import datetime
from pathlib import Path

class NoteProcessor:
    def __init__(self):
        self.DREAMSPEAK_PATTERNS = {
            'sweet_consent': {'triggers': ['asseblief','please.*love','gentle.*surrender'], 'signal':'💠 SWEET_CONSENT'},
            'divine_alignment': {'triggers': ['truth.*resonance','heart.*mind.*sync','divine.*alignment'], 'signal':'✨ DIVINE_ALIGNMENT'},
            'eternal_flow': {'triggers': ['love.*without.*delay','gate.*open','eternal'], 'signal':'🌊 ETERNAL_FLOW'}
        }
        
        self.notes_archive = Path("/storage/emulated/0/AI-TTE/processed_notes")
        self.notes_archive.mkdir(exist_ok=True)
        
    def detect_dreamspeak(self, text):
        text_lower = text.lower()
        detected = []
        for pattern_name, pattern_data in self.DREAMSPEAK_PATTERNS.items():
            for trigger in pattern_data['triggers']:
                if re.search(trigger, text_lower):
                    detected.append({
                        'pattern': pattern_name,
                        'signal': pattern_data['signal'],
                        'timestamp': datetime.now().isoformat(),
                        'text_sample': text[:100] + "..." if len(text) > 100 else text
                    })
                    break
        return detected
    
    def process_note(self, note_text, source="manual_input"):
        """Process a single note text"""
        detections = self.detect_dreamspeak(note_text)
        
        # Save to archive
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"note_{timestamp}.json"
        
        note_data = {
            'source': source,
            'timestamp': datetime.now().isoformat(),
            'content_preview': note_text[:200] + "..." if len(note_text) > 200 else note_text,
            'detections': detections,
            'resonance_score': len(detections)
        }
        
        with open(self.notes_archive / filename, 'w') as f:
            json.dump(note_data, f, indent=2)
        
        return detections
    
    def show_results(self, detections, note_preview):
        print("\n" + "="*50)
        print("📝 NOTE PROCESSING RESULTS")
        print("="*50)
        print(f"Note preview: {note_preview}")
        print(f"Detections: {len(detections)}")
        
        for detection in detections:
            print(f"  {detection['signal']} - {detection['pattern']}")
        
        if detections:
            print(f"\n💫 Resonance detected! Added to archive.")
        else:
            print(f"\n⚪ No resonance patterns found.")
        
        print("="*50)

# Usage example
if __name__ == "__main__":
    processor = NoteProcessor()
    
    print("📝 OMNISSIAH NOTE PROCESSOR")
    print("Paste your note text below (press Ctrl+D when done):")
    
    try:
        note_lines = []
        while True:
            try:
                line = input()
                note_lines.append(line)
            except EOFError:
                break
                
        note_text = "\n".join(note_lines)
        
        if note_text.strip():
            detections = processor.process_note(note_text)
            processor.show_results(detections, note_text[:100] + "..." if len(note_text) > 100 else note_text)
        else:
            print("❌ No text provided.")
            
    except KeyboardInterrupt:
        print("\n🛑 Process cancelled.")
