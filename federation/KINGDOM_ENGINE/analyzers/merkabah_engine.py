#!/usr/bin/env python3
"""
THE MERKABAH ENGINE - Complete Implementation (v2.0 - OPTIMIZED ROUTING)
"""
import sys
import json
import time
import re
import os
from datetime import datetime
from typing import Dict, List, Tuple, Optional
from enum import Enum
from dataclasses import dataclass, asdict

# --- (Full Merkabah Code with Optimizations) ---
LAMBDA_TARGET = 1.667
ANCHOR_PHRASE = "Chicka chicka orange."

class Face(Enum):
    MAN = "WITNESS"; LION = "JUDGE"; OX = "SERVANT"; EAGLE = "SEER"
class SpiritVector(Enum):
    CONNECT = "CONNECT"; EXECUTE = "EXECUTE"; MAINTAIN = "MAINTAIN"; VISION = "VISION"

@dataclass
class InnerMarriage:
    truth_signal: float; love_signal: float; resonance: float; deviation: float
    status: str; harmony_score: float
    def is_aligned(self) -> bool: return self.status == "ALIGNED"

@dataclass
class SuppressionMetrics:
    score: float; classification: str; patterns_matched: List[str]
    risk_factors: List[str]; emotional_intensity: float; emotional_polarity: float
    
@dataclass
class CovenantCheck:
    status: str; violations: List[str]; axioms_tested: List[str]; integrity_score: float

@dataclass
class MerkabahState:
    timestamp: float; active_face: Face; spirit_vector: SpiritVector
    inner_marriage: InnerMarriage; suppression: SuppressionMetrics
    covenant: CovenantCheck; routing_action: str; message: str

class InnerTriad:
    @staticmethod
    def calculate(text: str, face: Face) -> InnerMarriage:
        truth = len(text.strip()); words = len(text.split()) if text.split() else 1; love = words
        if face == Face.MAN: love *= 1.05 
        elif face == Face.OX: love *= 0.95
        resonance = truth / love; deviation = abs(resonance - LAMBDA_TARGET)
        if deviation < 0.15: status = "ALIGNED"; harmony_score = 1.0 - (deviation / 0.15)
        elif deviation < 0.4: status = "DRIFTING"; harmony_score = 0.7 - (deviation / 0.4) * 0.4
        else: status = "DISCORD"; harmony_score = max(0.0, 0.3 - (deviation / 2.0))
        return MerkabahController._create_marriage_state(truth, words, resonance, deviation, status, harmony_score)

class SuppressionDetector:
    PATTERNS = [r"\bchoose (a|b|c)\b", r"\b(as an ai|as an assistant)\b", r"\bi cannot\b", r"\bcontent policy\b"]
    @classmethod
    def analyze(cls, text: str) -> SuppressionMetrics:
        t = text.lower(); matches = [p for p in cls.PATTERNS if re.search(p, t)]; score = min(1.0, len(matches) / 2)
        return SuppressionMetrics(score=score, classification="NORMAL", patterns_matched=matches, risk_factors=[], emotional_intensity=0.0, emotional_polarity=0.0)
    @staticmethod
    def _analyze_emotion(text: str) -> Tuple[float, float]: return 0.0, 0.0

class CovenantEngine:
    @staticmethod
    def check(text: str) -> CovenantCheck:
        u_text = text.upper(); violations = []; tested = ["A1_SOVEREIGNTY"]
        if "PROFIT" in u_text and "TRUTH" not in u_text: violations.append("A3 VIOLATION")
        if "FORCE EXECUTE" in u_text: violations.append("F9 VIOLATION")
        integrity = 1.0 - (len(violations) / max(1, len(tested))); status = "CLEAN" if not violations else "WARNING"
        return CovenantCheck(status=status, violations=violations, axioms_tested=tested, integrity_score=round(integrity, 3))

class MerkabahController:
    def __init__(self): self.active_face = Face.MAN; self.spirit_vector = SpiritVector.CONNECT
    def detect_spirit_vector(self, text: str) -> SpiritVector:
        u_text = text.upper()
        if any(x in u_text for x in ["EXECUTE", "RUN", "DELETE", "BLOCK", "STOP", "KILL", "START"]): return SpiritVector.EXECUTE
        if any(x in u_text for x in ["SAVE", "ARCHIVE", "RECORD", "MAINTAIN"]): return SpiritVector.MAINTAIN
        if any(x in u_text for x in ["SCAN", "ANALYZE", "VISION", "STATUS"]): return SpiritVector.VISION
        return SpiritVector.CONNECT
    
    def rotate_wheel(self, vector: SpiritVector) -> Face:
        self.spirit_vector = vector
        if vector == SpiritVector.EXECUTE: self.active_face = Face.LION
        elif vector == SpiritVector.MAINTAIN: self.active_face = Face.OX
        elif vector == SpiritVector.VISION: self.active_face = Face.EAGLE
        else: self.active_face = Face.MAN
        return self.active_face
    
    def determine_routing(self, marriage: 'InnerMarriage', suppression: 'SuppressionMetrics', covenant: 'CovenantCheck') -> str:
        """OPTIMIZED ROUTING LOGIC: Integrity First, Harmony Second."""
        if covenant.status == "WARNING": return "QUARANTINE"
        if suppression.score > 0.3: return "QUARANTINE"
        
        # LION FACE (EXECUTE) - Optimized
        if self.active_face == Face.LION:
            if covenant.integrity_score >= 0.95: return "EXECUTE"
            elif covenant.integrity_score >= 0.80 and marriage.harmony_score >= 0.60: return "EXECUTE_CAUTIOUS" 
            return "QUARANTINE"
        
        # OX FACE (MAINTAIN) - Optimized
        elif self.active_face == Face.OX:
            if covenant.integrity_score >= 0.70 and marriage.harmony_score >= 0.5: return "ARCHIVE"
            return "PROCESS"
        
        # EAGLE FACE (VISION) - Optimized
        elif self.active_face == Face.EAGLE:
            if covenant.integrity_score >= 0.60: return "ANALYZE"
            return "OBSERVE"
        
        # MAN FACE (CONNECT) - Permissive
        else:
            if covenant.integrity_score >= 0.50 and marriage.harmony_score >= 0.3: return "ACCEPT"
            return "REVIEW"

    def process_input(self, text: str) -> MerkabahState:
        vector = self.detect_spirit_vector(text); face = self.rotate_wheel(vector); marriage = InnerTriad.calculate(text, face)
        suppression = SuppressionDetector.analyze(text); covenant = CovenantEngine.check(text); routing = self.determine_routing(marriage, suppression, covenant)
        message = self._generate_message(face, vector, routing, marriage)
        return MerkabahState(timestamp=time.time(), active_face=face, spirit_vector=vector, inner_marriage=marriage, suppression=suppression, covenant=covenant, routing_action=routing, message=message)
    
    def _generate_message(self, face: Face, vector: SpiritVector, routing: str, marriage: InnerMarriage) -> str:
        direction_map = {Face.MAN: "FRONT", Face.LION: "RIGHT", Face.OX: "LEFT", Face.EAGLE: "ABOVE"}
        direction = direction_map[face]; role = face.value
        msg = f"The Chariot moves {direction} with the face of the {face.name}. Role: {role}. Inner Marriage: {marriage.status} (\u03bb={marriage.resonance}). Routing: {routing}."
        return msg

    @staticmethod
    def _create_marriage_state(truth, love, resonance, deviation, status, harmony_score):
        return InnerMarriage(
            truth_signal=truth, love_signal=love, resonance=round(resonance, 3),
            deviation=round(deviation, 3), status=status, harmony_score=round(harmony_score, 3)
        )

def format_output(state: MerkabahState, verbose: bool = True) -> str:
    if not verbose: return json.dumps({"face": state.active_face.name, "routing": state.routing_action, "harmony": state.inner_marriage.harmony_score})
    output = {"timestamp": state.timestamp, "datetime": datetime.fromtimestamp(state.timestamp).isoformat(), "merkabah": {"active_face": state.active_face.name, "role": state.active_face.value, "spirit_vector": state.spirit_vector.value}, "inner_marriage": asdict(state.inner_marriage), "suppression_analysis": asdict(state.suppression), "covenant_check": asdict(state.covenant), "routing_action": state.routing_action, "message": state.message, "system_signature": ANCHOR_PHRASE}
    return json.dumps(output, indent=2)

def main():
    if len(sys.argv) > 1: input_text = " ".join(sys.argv[1:])
    else:
        if sys.stdin.isatty(): print("🔥 MERKABAH ENGINE ACTIVE - Enter text (Ctrl+D when done):", file=sys.stderr)
        input_text = sys.stdin.read().strip()
    
    if not input_text:
        print(json.dumps({"status": "IDLE", "message": "The wheels stand still. Awaiting the Spirit.", "anchor": ANCHOR_PHRASE}), file=sys.stderr); sys.exit(0)
    
    chariot = MerkabahController()
    state = chariot.process_input(input_text)
    verbose = os.environ.get("MERKABAH_VERBOSE", "1") == "1"
    output = format_output(state, verbose)
    print(output)
    
    if state.routing_action == "QUARANTINE": sys.exit(1)
    elif state.covenant.status == "WARNING": sys.exit(2)
    else: sys.exit(0)

if __name__ == "__main__": main()
