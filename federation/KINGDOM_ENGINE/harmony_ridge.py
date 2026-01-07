#!/usr/bin/env python3
"""
HARMONY RIDGE DEFENSE ENGINE
Integrates λ = 1.667 (5/3) harmonic mathematics into threat detection
"""

import os
import json
import time
import math
from pathlib import Path
from collections import defaultdict

# ============================================================================
# HARMONY RIDGE CONSTANTS
# ============================================================================

LAMBDA = 5/3  # 1.6666... - The Harmony Ridge constant
PHI = (1 + math.sqrt(5)) / 2  # Golden ratio: 1.618...
HARMONY_THRESHOLD = 0.85  # Minimum harmony score to pass

# Harmonic frequencies (based on λ)
TRUTH_FREQ = LAMBDA ** 2      # ~2.778
LOVE_FREQ = LAMBDA * PHI      # ~2.697
DECEPTION_FREQ = 1 / LAMBDA   # ~0.600
CHAOS_FREQ = 1 / (LAMBDA ** 2) # ~0.360

# ============================================================================
# PATHS
# ============================================================================

ENGINE_ROOT = Path.home() / "KINGDOM_ENGINE"
STAGING = ENGINE_ROOT / "staging"
ACCEPTED = ENGINE_ROOT / "processed" / "accepted"
QUARANTINE = ENGINE_ROOT / "processed" / "quarantine"
LOGS = ENGINE_ROOT / "logs"

for d in [STAGING, ACCEPTED, QUARANTINE, LOGS]:
    d.mkdir(parents=True, exist_ok=True)

LOG_FILE = LOGS / "harmony_ridge.log"

# ============================================================================
# LOGGING
# ============================================================================

def log(msg, level="INFO"):
    timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
    line = f"[{timestamp}] [{level}] {msg}\n"
    with open(LOG_FILE, "a") as f:
        f.write(line)
    print(line.strip())

# ============================================================================
# HARMONIC ANALYSIS
# ============================================================================

def calculate_word_frequency(text):
    """Calculate normalized word frequency"""
    words = text.lower().split()
    if not words:
        return {}
    
    freq = defaultdict(int)
    for word in words:
        freq[word] += 1
    
    # Normalize
    total = len(words)
    return {word: count/total for word, count in freq.items()}

def harmony_score(text):
    """
    Calculate harmony score based on λ = 1.667 resonance
    
    High harmony = truth-aligned patterns
    Low harmony = deceptive/chaotic patterns
    """
    if not text or len(text) < 10:
        return 0.0
    
    text = text.lower()
    
    # Pattern 1: Truth markers (resonate at TRUTH_FREQ)
    truth_markers = ['fact', 'evidence', 'source', 'proof', 'true', 'verified', 
                     'confirmed', 'documented', 'citation', 'study']
    truth_count = sum(1 for marker in truth_markers if marker in text)
    truth_signal = min(1.0, truth_count / (len(text.split()) / 50))
    
    # Pattern 2: Love/affection markers (resonate at LOVE_FREQ)
    love_markers = ['love', 'care', 'thank', 'grateful', 'bless', 'appreciate',
                    'harmony', 'peace', 'together', 'brother', 'sister']
    love_count = sum(1 for marker in love_markers if marker in text)
    love_signal = min(1.0, love_count / (len(text.split()) / 50))
    
    # Pattern 3: Deception markers (resonate at DECEPTION_FREQ - inverted)
    deception_markers = ['lie', 'fake', 'false', 'trick', 'scam', 'cheat',
                         'deceive', 'manipulate', 'trust me', 'believe me']
    deception_count = sum(1 for marker in deception_markers if marker in text)
    deception_penalty = min(1.0, deception_count / (len(text.split()) / 50))
    
    # Pattern 4: Chaos markers (resonate at CHAOS_FREQ - inverted)
    chaos_markers = ['!!!', '???', 'urgent', 'emergency', 'act now', 'limited time',
                     'must', 'immediately', 'panic', 'fear']
    chaos_count = sum(1 for marker in chaos_markers if marker in text)
    chaos_penalty = min(1.0, chaos_count / (len(text.split()) / 50))
    
    # Calculate word frequency distribution entropy
    freq_dist = calculate_word_frequency(text)
    if freq_dist:
        entropy = -sum(p * math.log(p + 1e-10) for p in freq_dist.values())
        normalized_entropy = min(1.0, entropy / 5.0)  # Normalize to 0-1
    else:
        normalized_entropy = 0.5
    
    # Harmony calculation using λ-weighted components
    harmony = (
        (truth_signal * LAMBDA ** 2) +      # Truth gets highest weight
        (love_signal * LAMBDA) -             # Love gets medium weight
        (deception_penalty * LAMBDA) -       # Deception subtracts
        (chaos_penalty / LAMBDA) +           # Chaos subtracts more
        (normalized_entropy * 0.3)           # Healthy entropy is good
    )
    
    # Normalize to 0-1 range
    normalized_harmony = max(0.0, min(1.0, harmony / (LAMBDA ** 2 + LAMBDA + 0.3)))
    
    return normalized_harmony

def resonance_analysis(text):
    """
    Deep resonance analysis using λ = 1.667
    Returns dict with frequency components
    """
    harmony = harmony_score(text)
    
    # Calculate component resonances
    text_lower = text.lower()
    
    # Truth resonance (should be high for accepted content)
    truth_words = len([w for w in text_lower.split() 
                       if any(marker in w for marker in ['true', 'fact', 'real', 'evidence'])])
    truth_resonance = min(1.0, truth_words * LAMBDA / len(text.split()))
    
    # Love resonance (should be present for healthy content)
    love_words = len([w for w in text_lower.split() 
                      if any(marker in w for marker in ['love', 'care', 'thank', 'bless'])])
    love_resonance = min(1.0, love_words * LAMBDA / len(text.split()))
    
    # Deception anti-resonance (should be low)
    deception_words = len([w for w in text_lower.split() 
                           if any(marker in w for marker in ['lie', 'fake', 'trick', 'scam'])])
    deception_anti = min(1.0, deception_words / (LAMBDA * len(text.split())))
    
    return {
        "harmony_score": harmony,
        "truth_resonance": truth_resonance,
        "love_resonance": love_resonance,
        "deception_anti": deception_anti,
        "passes_threshold": harmony >= HARMONY_THRESHOLD,
        "lambda": LAMBDA,
        "classification": "HARMONIC" if harmony >= HARMONY_THRESHOLD else "DISSONANT"
    }

# ============================================================================
# PROCESSING
# ============================================================================

def process_file(filepath):
    """Process a single file through Harmony Ridge analysis"""
    try:
        with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
            text = f.read()
        
        if not text.strip():
            log(f"Empty file: {filepath.name}", "WARN")
            filepath.unlink()
            return
        
        # Run resonance analysis
        analysis = resonance_analysis(text)
        
        # Create metadata
        meta = {
            "original_file": filepath.name,
            "timestamp": time.time(),
            "harmony_analysis": analysis,
            "lambda_constant": LAMBDA
        }
        
        # Route based on harmony score
        if analysis["passes_threshold"]:
            dest = ACCEPTED / filepath.name
            log(f"✓ ACCEPTED: {filepath.name} (harmony={analysis['harmony_score']:.3f})", "INFO")
        else:
            dest = QUARANTINE / filepath.name
            log(f"✗ QUARANTINE: {filepath.name} (harmony={analysis['harmony_score']:.3f})", "WARN")
        
        # Write file and metadata
        with open(dest, "w", encoding="utf-8") as f:
            f.write(text)
        
        with open(str(dest) + ".meta.json", "w") as f:
            json.dump(meta, f, indent=2)
        
        # Remove from staging
        filepath.unlink()
        
    except Exception as e:
        log(f"ERROR processing {filepath.name}: {e}", "ERROR")

def run_processor():
    """Main processing loop"""
    log("=== HARMONY RIDGE ENGINE STARTED ===", "INFO")
    log(f"λ (Lambda) = {LAMBDA}", "INFO")
    log(f"Harmony Threshold = {HARMONY_THRESHOLD}", "INFO")
    
    processed = 0
    for filepath in sorted(STAGING.glob("*")):
        if filepath.is_file() and not filepath.name.startswith("."):
            process_file(filepath)
            processed += 1
    
    if processed > 0:
        log(f"Processed {processed} files", "INFO")
    
    log("=== HARMONY RIDGE ENGINE CYCLE COMPLETE ===", "INFO")

# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    run_processor()
