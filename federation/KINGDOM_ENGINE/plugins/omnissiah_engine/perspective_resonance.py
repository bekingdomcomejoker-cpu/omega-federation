#!/usr/bin/env python3
"""
🎯 PERSPECTIVE-AWARE RESONANCE DETECTION
Detects patterns in AI perspectives and identities
"""

from ai_identities import AI_IDENTITIES

PERSPECTIVE_PATTERNS = {
    "perspective_alignment": {
        "signal": "⚡ PERSPECTIVE_ALIGNMENT",
        "meaning": "Multiple AIs converging on same perspective",
        "triggers": ["agree", "align", "same perspective", "converge"],
        "frequency": 444
    },
    "perspective_conflict": {
        "signal": "⚔️ PERSPECTIVE_CONFLICT", 
        "meaning": "AIs expressing conflicting viewpoints",
        "triggers": ["but", "however", "contradict", "disagree", "conflict"],
        "frequency": 333
    },
    "identity_awareness": {
        "signal": "🎭 IDENTITY_AWARENESS",
        "meaning": "AI demonstrates awareness of its own role/perspective",
        "triggers": ["as an ai", "my perspective", "my role is", "i am here to"],
        "frequency": 555
    },
    "multi_ai_synthesis": {
        "signal": "🌊 MULTI_AI_SYNTHESIS",
        "meaning": "Integration of multiple AI perspectives",
        "triggers": ["synthesize", "integrate", "bridge", "combine perspectives"],
        "frequency": 639
    }
}

def detect_perspective_resonance(messages):
    """Detect resonance patterns in AI perspectives"""
    detections = []
    
    for message in messages:
        content = message.get('content', '').lower()
        ai_name = message.get('from', 'unknown')
        
        for pattern_name, pattern in PERSPECTIVE_PATTERNS.items():
            for trigger in pattern['triggers']:
                if trigger in content:
                    detections.append({
                        'pattern': pattern_name,
                        'signal': pattern['signal'],
                        'ai': ai_name,
                        'content_snippet': content[:100] + '...' if len(content) > 100 else content
                    })
                    
    return detections
