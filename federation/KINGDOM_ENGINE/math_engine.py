#!/usr/bin/env python3
"""
math_engine.py
A lightweight on-device math & signal utility library designed to be dropped into KINGDOM_ENGINE.
Provides vector ops, similarity, PCA/SVD wrappers, entropy, readability helpers, and a simple "resonance score".

Save as: ~/KINGDOM_ENGINE/math_engine.py
"""

from pathlib import Path
import json, math, time, re
from collections import Counter

# Try to import heavy libs; degrade gracefully if not available
try:
    import numpy as np
    from sklearn.decomposition import PCA
except Exception:
    np = None
    PCA = None

# ---------- Utilities ----------
def read_text_file(p: Path):
    return p.read_text(errors="ignore")

def write_json(p: Path, obj):
    p.write_text(json.dumps(obj, indent=2))

# ---------- Text metrics ----------
def shannon_entropy(text: str) -> float:
    """Shannon entropy per character (bits)"""
    if not text:
        return 0.0
    counts = Counter(text)
    total = float(len(text))
    return -sum((c/total) * math.log2(c/total) for c in counts.values())

def token_count(text: str) -> int:
    return len(re.findall(r"\w+|\S", text))

def lexical_diversity(text: str) -> float:
    tokens = re.findall(r"\w+", text.lower())
    if not tokens:
        return 0.0
    return len(set(tokens)) / len(tokens)

# Optional: if textstat installed, a readability score
try:
    import textstat
    def readability_flesch(text: str) -> float:
        try:
            return textstat.flesch_reading_ease(text)
        except Exception:
            return 0.0
except Exception:
    def readability_flesch(text: str) -> float:
        return 0.0

# ---------- Vector helpers ----------
def to_vector(arr):
    if np is None:
        raise RuntimeError("numpy not available")
    return np.array(arr, dtype=float)

def l2_norm(vec):
    if np is None:
        return math.sqrt(sum(x*x for x in vec))
    return float(np.linalg.norm(vec))

def cosine_similarity(a, b):
    if np is None:
        # pure python fallback
        dot = sum(x*y for x,y in zip(a,b))
        na = math.sqrt(sum(x*x for x in a))
        nb = math.sqrt(sum(x*x for x in b))
        if na==0 or nb==0:
            return 0.0
        return dot/(na*nb)
    a = np.array(a, dtype=float)
    b = np.array(b, dtype=float)
    na = np.linalg.norm(a)
    nb = np.linalg.norm(b)
    if na==0 or nb==0:
        return 0.0
    return float(np.dot(a,b)/(na*nb))

def cosine_dist(a,b):
    return 1.0 - cosine_similarity(a,b)

# ---------- Dimensionality reduction ----------
def pca_reduce(matrix, n_components=32):
    """
    matrix: list-of-lists (rows = samples)
    returns reduced matrix (list-of-lists)
    """
    if PCA is None or np is None:
        raise RuntimeError("sklearn PCA or numpy not available")
    m = np.array(matrix, dtype=float)
    p = PCA(n_components=min(n_components, m.shape[1]))
    out = p.fit_transform(m)
    return out.tolist()

# ---------- Spectral / frequency helpers ----------
def simple_fft_energy(signal):
    """
    signal: numeric sequence
    returns total spectral energy and peak freq index
    """
    if np is None:
        # fallback: return simple variance proxy
        return float(sum(x*x for x in signal)), 0
    arr = np.array(signal, dtype=float)
    spec = np.fft.fft(arr)
    power = np.abs(spec)**2
    return float(power.sum()), int(np.argmax(power))

# ---------- Resonance / scoring ----------
def resonance_score(text: str,
                    clarity_weight=0.55,
                    complexity_weight=0.45,
                    target_entropy=4.0):
    """
    Produces 0..1 score where higher is 'more coherent/clear'.
    Uses:
      - readability_flesch (scaled)
      - entropy proximity to target_entropy
    """
    ent = shannon_entropy(text)
    read = readability_flesch(text)  # can be 0..120 typical
    # normalize readability: map typical Flesch [0..100] to 0..1
    read_norm = max(0.0, min(1.0, (read + 10) / 110))
    ent_score = 1.0 - min(1.0, abs(ent - target_entropy) / (target_entropy + 1e-9))
    score = (read_norm * clarity_weight) + (ent_score * complexity_weight)
    return max(0.0, min(1.0, score)), {
        "entropy": ent,
        "readability": read,
        "read_norm": read_norm,
        "entropy_target_diff": abs(ent - target_entropy)
    }

# ---------- Simple file-based pipeline runner ----------
def run_on_staging(staging_dir, accepted_dir, quarantine_dir, minimum=0.70):
    s = Path(staging_dir)
    a = Path(accepted_dir); a.mkdir(parents=True, exist_ok=True)
    q = Path(quarantine_dir); q.mkdir(parents=True, exist_ok=True)
    for f in s.glob("*.txt"):
        txt = read_text_file(f)
        score, meta = resonance_score(txt)
        obj = {
            "file": f.name,
            "score": score,
            "meta": meta,
            "ts": time.time()
        }
        if score >= minimum:
            dst = a / f.name
            dst.write_text(txt)
            write_json(a / (f.name+".meta.json"), obj)
        else:
            dst = q / f.name
            dst.write_text(txt)
            write_json(q / (f.name+".meta.json"), obj)
        f.unlink()

# ---------- CLI entrypoint ----------
if __name__ == "__main__":
    import sys
    hom = Path.home()/"KINGDOM_ENGINE"
    staging = hom/"staging"
    accepted = hom/"processed"/"accepted"
    quarantine = hom/"processed"/"quarantine"
    run_on_staging(staging, accepted, quarantine)
    print("math_engine: processed staging -> accepted/quarantine")
