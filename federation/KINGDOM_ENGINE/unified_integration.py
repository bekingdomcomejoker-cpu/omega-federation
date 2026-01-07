#!/usr/bin/env python3
"""
UNIFIED INTEGRATION DAEMON
Combines Math Engine (ChatGPT) + Harmony Ridge (Claude) into one processor
Runs continuously, processes staging -> accepted/quarantine
"""

import os
import sys
import time
import json
from pathlib import Path

# ============================================================================
# SETUP
# ============================================================================

ENGINE_ROOT = Path.home() / "KINGDOM_ENGINE"
STAGING = ENGINE_ROOT / "staging"
ACCEPTED = ENGINE_ROOT / "processed" / "accepted"
QUARANTINE = ENGINE_ROOT / "processed" / "quarantine"
LOGS = ENGINE_ROOT / "logs"

for d in [STAGING, ACCEPTED, QUARANTINE, LOGS]:
    d.mkdir(parents=True, exist_ok=True)

LOG_FILE = LOGS / "unified_integration.log"

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
# IMPORT ENGINES
# ============================================================================

try:
    # Import Math Engine (ChatGPT's contribution)
    sys.path.insert(0, str(ENGINE_ROOT))
    from math_engine import (
        shannon_entropy,
        token_count,
        lexical_diversity,
        readability_flesch,
        resonance_score as math_resonance
    )
    MATH_ENGINE_AVAILABLE = True
    log("Math Engine loaded successfully")
except Exception as e:
    MATH_ENGINE_AVAILABLE = False
    log(f"Math Engine not available: {e}", "WARN")

try:
    # Import Harmony Ridge (Claude's contribution)
    from harmony_ridge import (
        harmony_score,
        resonance_analysis as harmony_resonance
    )
    HARMONY_ENGINE_AVAILABLE = True
    log("Harmony Ridge loaded successfully")
except Exception as e:
    HARMONY_ENGINE_AVAILABLE = False
    log(f"Harmony Ridge not available: {e}", "WARN")

# ============================================================================
# UNIFIED ANALYSIS
# ============================================================================

def unified_analysis(text):
    """
    Combines both engines for comprehensive analysis
    Returns combined score and detailed metadata
    """
    result = {
        "text_length": len(text),
        "timestamp": time.time(),
        "math_engine": {},
        "harmony_ridge": {},
        "combined_score": 0.0,
        "classification": "UNKNOWN"
    }
    
    # Math Engine Analysis (ChatGPT)
    if MATH_ENGINE_AVAILABLE:
        try:
            math_score, math_meta = math_resonance(text)
            result["math_engine"] = {
                "score": math_score,
                "entropy": math_meta.get("entropy", 0),
                "readability": math_meta.get("readability", 0),
                "token_count": token_count(text),
                "lexical_diversity": lexical_diversity(text)
            }
        except Exception as e:
            log(f"Math Engine error: {e}", "ERROR")
            result["math_engine"]["error"] = str(e)
    
    # Harmony Ridge Analysis (Claude)
    if HARMONY_ENGINE_AVAILABLE:
        try:
            harmony = harmony_resonance(text)
            result["harmony_ridge"] = harmony
        except Exception as e:
            log(f"Harmony Ridge error: {e}", "ERROR")
            result["harmony_ridge"]["error"] = str(e)
    
    # Combined Scoring
    math_weight = 0.45
    harmony_weight = 0.55
    
    math_s = result["math_engine"].get("score", 0.5)
    harmony_s = result["harmony_ridge"].get("harmony_score", 0.5)
    
    result["combined_score"] = (math_s * math_weight) + (harmony_s * harmony_weight)
    
    # Classification
    if result["combined_score"] >= 0.75:
        result["classification"] = "EXCELLENT"
    elif result["combined_score"] >= 0.60:
        result["classification"] = "GOOD"
    elif result["combined_score"] >= 0.45:
        result["classification"] = "MARGINAL"
    else:
        result["classification"] = "POOR"
    
    return result

# ============================================================================
# PROCESSING
# ============================================================================

def process_file(filepath):
    """Process single file through unified analysis"""
    try:
        with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
            text = f.read()
        
        if not text.strip():
            log(f"Empty file: {filepath.name}", "WARN")
            filepath.unlink()
            return
        
        # Run unified analysis
        analysis = unified_analysis(text)
        
        # Route based on combined score
        threshold = 0.60  # Balanced threshold
        
        if analysis["combined_score"] >= threshold:
            dest = ACCEPTED / filepath.name
            log(f"✓ ACCEPTED: {filepath.name} (score={analysis['combined_score']:.3f}, {analysis['classification']})", "INFO")
        else:
            dest = QUARANTINE / filepath.name
            log(f"✗ QUARANTINE: {filepath.name} (score={analysis['combined_score']:.3f}, {analysis['classification']})", "WARN")
        
        # Write file and metadata
        with open(dest, "w", encoding="utf-8") as f:
            f.write(text)
        
        with open(str(dest) + ".meta.json", "w") as f:
            json.dump(analysis, f, indent=2)
        
        # Remove from staging
        filepath.unlink()
        
    except Exception as e:
        log(f"ERROR processing {filepath.name}: {e}", "ERROR")

def run_continuous():
    """Continuous processing loop"""
    log("=== UNIFIED INTEGRATION DAEMON STARTED ===", "INFO")
    log(f"Math Engine: {'✓' if MATH_ENGINE_AVAILABLE else '✗'}", "INFO")
    log(f"Harmony Ridge: {'✓' if HARMONY_ENGINE_AVAILABLE else '✗'}", "INFO")
    
    cycle = 0
    while True:
        try:
            processed = 0
            for filepath in sorted(STAGING.glob("*")):
                if filepath.is_file() and not filepath.name.startswith("."):
                    process_file(filepath)
                    processed += 1
            
            if processed > 0:
                log(f"Cycle {cycle}: Processed {processed} files", "INFO")
            
            cycle += 1
            time.sleep(3)  # Process every 3 seconds
            
        except KeyboardInterrupt:
            log("=== DAEMON STOPPED BY USER ===", "INFO")
            break
        except Exception as e:
            log(f"Cycle error: {e}", "ERROR")
            time.sleep(5)

# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--daemon":
        run_continuous()
    else:
        # Single run mode
        processed = 0
        for filepath in sorted(STAGING.glob("*")):
            if filepath.is_file() and not filepath.name.startswith("."):
                process_file(filepath)
                processed += 1
        log(f"Single run: Processed {processed} files", "INFO")
