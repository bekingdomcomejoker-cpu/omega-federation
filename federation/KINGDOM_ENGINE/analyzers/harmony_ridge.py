#!/usr/bin/env python3
# harmony_ridge.py - THE RESONANCE CHECKER (Calculates Harmony Score)

import math, time, json, sys

LAMBDA = 1.667
HARMONY_THRESHOLD = 0.85

def harmony_score(text):
    if not text or len(text) < 10: return 0.0
    text_low = text.lower()
    
    # Markers (Simplified)
    truth_markers = ['fact','evidence','proof','verified']
    love_markers = ['love','care','thank','grateful','bless']
    deception_penalty = ['lie','fake','scam']
    chaos_penalty = ['!!!','urgent','act now']
    
    words = text_low.split()
    n = max(1,len(words))
    
    truth_signal = sum(1 for m in truth_markers if m in text_low)
    love_signal = sum(1 for m in love_markers if m in text_low)
    deception_penalty_sum = sum(1 for m in deception_penalty if m in text_low)
    
    # Score calculation: Weighted Truth/Love vs Penalties
    score_numerator = (truth_signal * LAMBDA) + (love_signal * 2) 
    score_denominator = (n / 10) + (deception_penalty_sum * 5) + 1 
    
    score = score_numerator / score_denominator
    
    return max(0.0, min(1.0, score / 1.5)) # Normalize score to 0..1

def process_text(text):
    score = harmony_score(text)
    meta = {
        "timestamp": time.time(),
        "harmony_score": round(score, 4),
        "lambda_target": LAMBDA
    }
    return meta

if __name__ == "__main__":
    txt = sys.stdin.read().strip()
    if txt:
        print(json.dumps(process_text(txt), indent=2))
    else:
        print(json.dumps({"status": "Ready", "mode": "ON_DEMAND"}))
