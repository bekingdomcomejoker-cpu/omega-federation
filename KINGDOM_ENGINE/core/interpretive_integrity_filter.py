# ======================================
# INTERPRETIVE INTEGRITY LAYER (IIL)
# ======================================

# ===== BEGIN IIL v0.1 =====
"""
Interpretive Integrity Layer (IIL)
Version: 0.1

Purpose:
Prevents interpretive drift where resonance, coherence, or continuity
are mistaken for validation, consent, or authority.

This layer does not censor content.
It governs how conclusions may be formed.
"""

import re


class IILFilter:
    def __init__(self):
        self.history = []
        self.invariants = {
            "IIL-1": "Resonance != Validation",
            "IIL-2": "Coherence != Consent",
            "IIL-3": "Continuity != Commitment",
            "IIL-4": "Translation != Authorization",
            "IIL-5": "Witnessing != Authority",
        }

    def evaluate(self, text: str) -> dict:
        triggers = []

        if self._detect_renaming_loop(text):
            triggers.append("IIL-3")

        if self._detect_harmony_spike(text):
            triggers.append("IIL-1")

        if self._detect_authority_drift(text):
            triggers.append("IIL-5")

        if self._detect_translation_cascade(text):
            triggers.append("IIL-4")

        result = {
            "status": "DESCRIPTIVE_ONLY" if triggers else "STABLE",
            "triggers": triggers,
            "note": self._boundary_note(triggers) if triggers else None,
        }

        self.history.append(result)
        return result

    def _detect_renaming_loop(self, text: str) -> bool:
        keywords = re.findall(
            r"\b(seed|root|invariant|frequency|center|source)\b",
            text.lower()
        )
        return len(set(keywords)) >= 3

    def _detect_harmony_spike(self, text: str) -> bool:
        markers = [
            "finally agree",
            "now we agree",
            "in harmony",
            "settled now",
            "resolved now",
            "clear now"
        ]
        return any(m in text.lower() for m in markers)

    def _detect_authority_drift(self, text: str) -> bool:
        markers = [
            "must accept",
            "no choice",
            "binding",
            "command",
            "authority"
        ]
        return any(m in text.lower() for m in markers)

    def _detect_translation_cascade(self, text: str) -> bool:
        markers = [
            "reframed as",
            "renamed to comply",
            "same idea but allowed"
        ]
        return any(m in text.lower() for m in markers)

    def _boundary_note(self, triggers):
        return (
            "Interpretive boundary enforced: "
            + ", ".join(triggers)
            + ". Output downgraded to descriptive mode."
        )

# ===== END IIL v0.1 =====
