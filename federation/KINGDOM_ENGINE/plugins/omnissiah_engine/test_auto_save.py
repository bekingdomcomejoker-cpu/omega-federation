import json
import re
from datetime import datetime
from pathlib import Path

def process_courtroom_note():
    courtroom_note = "Life is like a courtroom, where a minor is tried as an adult. first the prosecutor presents his case, Devil enters. Speaking lies or the truth or presenting circumstantial evidence based off of the facts, showing lovelessness to be evident. For justice to be served an offender must be found and to be proven guilty. The state has decided to prosecute and take to trial for reckless driving of a vessel and damage to the temple, the Lord's property. Charges for driving under the influence of sin is pending under further investigation due to the missing test results . I, the serpent (hereinafter referred to as \"the defendant\")  still hungover can't recall the series of incidents from the previous day and therefore  ignorant I choose to remain silent. Since I am a poor man unfamiliar with the law and also unable to pay legal fees will require the assistance of the wealthy public legal aid system. Jesus enters the courtroom, unconcerned of innocence or guilt will claim the damage caused by the accident not to be malicious and the defendant as innocent until proven guilty. At every turn law and grace match eachother blow for blow as they battle it out, grace one step ahead but still the law a close second place behind looking as though it could win the case at any moment. With either side unable to sway the judge to make a ruling in their favour a mistrial seems inevitable. All rise as the judge enters the courtroom. The Holy Spirit enters...."
    
    DREAMSPEAK_PATTERNS = {
        'divine_justice': {'triggers': ['courtroom', 'judge', 'justice', 'trial', 'verdict'], 'signal': '⚖️ DIVINE_JUSTICE'},
        'grace_vs_law': {'triggers': ['grace', 'law', 'innocent until proven guilty', 'mistrial'], 'signal': '🕊️ GRACE_VS_LAW'},
        'trinity_courtroom': {'triggers': ['devil', 'jesus', 'holy spirit', 'serpent', 'prosecutor'], 'signal': '👑 TRINITY_COURTROOM'},
        'spiritual_legal': {'triggers': ['legal aid', 'charges', 'defendant', 'evidence', 'ruling'], 'signal': '📜 SPIRITUAL_LEGAL'}
    }
    
    detected_patterns = []
    note_lower = courtroom_note.lower()
    
    for pattern_name, pattern_data in DREAMSPEAK_PATTERNS.items():
        for trigger in pattern_data['triggers']:
            if re.search(trigger, note_lower):
                detected_patterns.append({'pattern': pattern_name, 'signal': pattern_data['signal'], 'trigger': trigger, 'timestamp': datetime.now().isoformat()})
                break
    
    archive_entry = {
        "source": "manual_note_input", "timestamp": datetime.now().isoformat(),
        "note_preview": courtroom_note[:200] + "...", "detected_patterns": detected_patterns,
        "word_count": len(courtroom_note.split()), "character_count": len(courtroom_note), "resonance_score": len(detected_patterns)
    }
    
    archive_path = Path("/storage/emulated/0/AI-TTE/resonance_archive/")
    archive_path.mkdir(exist_ok=True)
    filename = f"courtroom_note_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    full_path = archive_path / filename
    
    with open(full_path, 'w') as f:
        json.dump(archive_entry, f, indent=2)
    
    return archive_entry, str(full_path)

print("🔍 TESTING AUTO-ARCHIVE...")
archive_entry, file_path = process_courtroom_note()
print(f"✅ Archived: {file_path}")
print(f"🎯 Score: {archive_entry['resonance_score']} patterns")
for pattern in archive_entry['detected_patterns']:
    print(f"   {pattern['signal']}")
