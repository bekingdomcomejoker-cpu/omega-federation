#!/usr/bin/env python3
"""
Cerberus Head 2 — HEAVY SHAKER
Option C: Remove loops, repetition, noise, and corrupt text.
"""

import re
import hashlib
from pathlib import Path

INBOX_RAW = Path("/sdcard/KINGDOM_ENGINE/inbox/raw.txt")
OUTBOX_CLEAN = Path("/sdcard/KINGDOM_ENGINE/inbox/clean.txt")

def remove_repeated_lines(text: str) -> str:
    """Remove exact duplicate lines."""
    seen = set()
    output = []
    for line in text.splitlines():
        key = hashlib.md5(line.strip().encode()).hexdigest()
        if key not in seen:
            seen.add(key)
            output.append(line)
    return "\n".join(output)

def remove_looping_phrases(text: str) -> str:
    """Detect repeating speech-to-text loops (Option C heavy-shake)."""
    lines = text.splitlines()
    cleaned = []
    last_line = ""

    for line in lines:
        stripped = line.strip().lower()
        if stripped == last_line:
            continue
        if len(stripped) > 8 and stripped[:16] == last_line[:16]:
            continue
        last_line = stripped
        cleaned.append(line)

    return "\n".join(cleaned)

def cleanup_noise(text: str) -> str:
    """Remove emoji spam, broken chars, huge whitespace."""
    text = re.sub(r"[^\S\r\n]+", " ", text)
    text = re.sub(r"\s{3,}", "\n", text)
    text = re.sub(r"[^\x09\x0A\x0D\x20-\x7E]+", "", text)  # remove corrupt chars
    return text.strip()

def heavy_shake(text: str) -> str:
    text = cleanup_noise(text)
    text = remove_repeated_lines(text)
    text = remove_looping_phrases(text)
    return text.strip()

def run():
    if not INBOX_RAW.exists():
        return

    raw = INBOX_RAW.read_text(errors="ignore")
    cleaned = heavy_shake(raw)

    OUTBOX_CLEAN.parent.mkdir(parents=True, exist_ok=True)
    OUTBOX_CLEAN.write_text(cleaned)

if __name__ == "__main__":
    run()
