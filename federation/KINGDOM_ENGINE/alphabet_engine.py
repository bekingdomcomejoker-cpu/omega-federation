#!/usr/bin/env python3
"""
alphabet_engine.py
Alphabet / symbol encoder and lightweight vector index.

Save as: ~/KINGDOM_ENGINE/alphabet_engine.py
Requires: ~/KINGDOM_ENGINE/math_engine.py available and importable.

Features:
- build / load alphabet map
- encode text -> fixed-size vector (simple, tunable)
- small vector store (file-backed JSON)
- brute-force nearest neighbors (cosine)
- CLI: build-map, encode-file, add-to-index, search
"""

from pathlib import Path
import json, math, time, re
from collections import Counter, defaultdict

# Import the math primitives we wrote earlier.
try:
    from math_engine import (
        shannon_entropy, token_count, lexical_diversity,
        readability_flesch, cosine_similarity,
        to_vector, l2_norm
    )
except Exception as e:
    raise SystemExit("Require math_engine.py in the same folder or PYTHONPATH. Error: " + str(e))

# --------- Config / Paths ----------
HOME = Path.home() / "KINGDOM_ENGINE"
CONFIG_PATH = HOME / "alphabet_config.json"
INDEX_PATH = HOME / "alphabet_index.json"
DEFAULT_VECTOR_SIZE = 128

# --------- Default Alphabet Map (example)
# This map can be fully customized by user. Keeps tokens -> base weight.
DEFAULT_MAP = {
    # basic ASCII letters mapped to tier weights (example)
    **{c: 1.0 for c in "abcdefghijklmnopqrstuvwxyz"},
    # vowels slightly boosted
    **{c: 1.3 for c in "aeiou"},
    # digits
    **{str(i): 0.9 for i in range(10)},
    # punctuation specials
    ".": 0.5, ",": 0.5, "!": 0.3, "?": 0.3, "-": 0.2, "_": 0.2
}

# If user wants to include other language alphabets, they can edit the config file.

# --------- Helpers ----------
def load_config():
    if CONFIG_PATH.exists():
        return json.loads(CONFIG_PATH.read_text())
    cfg = {
        "vector_size": DEFAULT_VECTOR_SIZE,
        "alphabet_map": DEFAULT_MAP,
        "token_split_regex": r"\w+|[^\s\w]",
        "normalization": "lower",
        "entropy_target": 4.0
    }
    CONFIG_PATH.write_text(json.dumps(cfg, indent=2))
    return cfg

def save_config(cfg):
    CONFIG_PATH.write_text(json.dumps(cfg, indent=2))

def load_index():
    if INDEX_PATH.exists():
        return json.loads(INDEX_PATH.read_text())
    idx = {"items": []}
    INDEX_PATH.write_text(json.dumps(idx, indent=2))
    return idx

def save_index(idx):
    INDEX_PATH.write_text(json.dumps(idx, indent=2))

# --------- Tokenization & normalization ----------
def tokenize(text, regex=None, normalization="lower"):
    if normalization == "lower":
        text = text.lower()
    pat = re.compile(regex or r"\w+|[^\s\w]", flags=re.UNICODE)
    return pat.findall(text)

# --------- Encoding: token -> vector
def build_seed_vector_from_map(alphabet_map, size):
    """
    Build deterministic pseudo-random seed vectors for each token key
    using a hash -> numeric sequence. This avoids heavy libs and is reproducible.
    Returns dict token -> list[float] length=size
    """
    seeds = {}
    # simple hash to float generator for reproducible random-like vectors
    def token_to_seed_vector(token, size):
        base = 2166136261  # FNV offset basis
        for ch in token:
            base = (base ^ ord(ch)) * 16777619 & 0xFFFFFFFF
        # create values by iterating LCG
        vals = []
        a = 1664525; c = 1013904223; m = 2**32
        state = base or 1
        for _ in range(size):
            state = (a * state + c) % m
            # map to -1..1 float
            vals.append(((state / m) * 2.0) - 1.0)
        # normalize to unit length
        norm = math.sqrt(sum(x*x for x in vals)) or 1.0
        return [float(x / norm) for x in vals]

    for t in alphabet_map.keys():
        seeds[t] = token_to_seed_vector(t, size)
    return seeds

def encode_text_to_vector(text, cfg=None, seed_vectors=None):
    """
    Encode text to fixed-size vector.
    Method:
     - tokenize
     - weight tokens by alphabet_map weights and local frequency
     - sum weighted seed vectors, l2-normalize
     - add lightweight metadata features (entropy, readability) mapped into small dims
    """
    cfg = cfg or load_config()
    vsz = cfg.get("vector_size", DEFAULT_VECTOR_SIZE)
    amap = cfg.get("alphabet_map", DEFAULT_MAP)
    regex = cfg.get("token_split_regex")
    tokens = tokenize(text, regex=regex, normalization=cfg.get("normalization", "lower"))
    if not tokens:
        return [0.0]*vsz

    # Build or accept seed vectors
    if seed_vectors is None:
        seed_vectors = build_seed_vector_from_map(amap, vsz)

    # compute token frequencies
    freqs = Counter(tokens)
    total_tokens = sum(freqs.values())

    # accumulate vector
    acc = [0.0]*vsz
    for tok, f in freqs.items():
        # token base weight lookup: exact token or fallback to char-level weighting
        w = amap.get(tok)
        if w is None:
            # try char-level average
            if len(tok) == 1:
                w = amap.get(tok, 0.5)
            else:
                # average char weights
                chars = [amap.get(ch, 0.4) for ch in tok]
                w = sum(chars)/len(chars) if chars else 0.4
        # frequency factor (diminishing returns)
        freq_factor = 1.0 + math.log1p(f)
        # contribution vector
        sv = seed_vectors.get(tok)
        if sv is None:
            # fallback generate from token
            sv = build_seed_vector_from_map({tok:0}, vsz)[tok]
        scale = w * freq_factor
        for i in range(vsz):
            acc[i] += sv[i] * scale

    # Normalize accumulated vector
    norm = math.sqrt(sum(x*x for x in acc)) or 1.0
    acc = [float(x / norm) for x in acc]

    # Append small metadata injection into tail of vector if space permits
    # We'll mix entropy & readability small signals into last 4 dims
    ent = shannon_entropy(text)
    read = readability_flesch(text)
    # map to -1..1
    ent_m = ((ent % 8) / 8.0) * 2 - 1  # rough wrap
    read_m = ((read % 120) / 120.0) * 2 - 1
    # inject into last two dims if vector is long enough
    if vsz >= 4:
        acc[-1] = (acc[-1] + ent_m) / 2.0
        acc[-2] = (acc[-2] + read_m) / 2.0

    # final re-normalize
    norm = math.sqrt(sum(x*x for x in acc)) or 1.0
    acc = [float(x / norm) for x in acc]
    return acc

# --------- Index management ----------
def index_add_item(item_id, text, cfg=None):
    cfg = cfg or load_config()
    idx = load_index()
    # build seed table once for map tokens
    seed_vectors = build_seed_vector_from_map(cfg.get("alphabet_map", DEFAULT_MAP), cfg.get("vector_size", DEFAULT_VECTOR_SIZE))
    vec = encode_text_to_vector(text, cfg=cfg, seed_vectors=seed_vectors)
    item = {
        "id": item_id,
        "ts": time.time(),
        "text_snippet": text[:300],
        "vector": vec
    }
    # remove any existing item with same id
    idx["items"] = [it for it in idx.get("items", []) if it.get("id") != item_id]
    idx["items"].append(item)
    save_index(idx)
    return item

def index_search_vector(query_vec, top_n=6):
    idx = load_index()
    out = []
    for it in idx.get("items", []):
        v = it.get("vector", [])
        try:
            sim = cosine_similarity(query_vec, v)
        except Exception:
            sim = 0.0
        out.append((sim, it))
    out.sort(key=lambda x: x[0], reverse=True)
    return out[:top_n]

def index_search_text(query_text, cfg=None, top_n=6):
    cfg = cfg or load_config()
    seed_vectors = build_seed_vector_from_map(cfg.get("alphabet_map", DEFAULT_MAP), cfg.get("vector_size", DEFAULT_VECTOR_SIZE))
    qv = encode_text_to_vector(query_text, cfg=cfg, seed_vectors=seed_vectors)
    return index_search_vector(qv, top_n=top_n)

# --------- Cross-language frequency helpers ----------
def token_frequency_map(text, regex=None, normalization="lower"):
    tokens = tokenize(text, regex=regex, normalization=normalization)
    c = Counter(tokens)
    total = sum(c.values()) or 1
    return {t: v/total for t,v in c.items()}

def pairwise_token_overlap(a_text, b_text, regex=None):
    amap = token_frequency_map(a_text, regex=regex)
    bmap = token_frequency_map(b_text, regex=regex)
    overlap = 0.0
    for t,v in amap.items():
        overlap += v * bmap.get(t, 0.0)
    return overlap  # 0..1 probability-like

# --------- CLI Entrypoint ----------
def _print_json(obj):
    print(json.dumps(obj, indent=2))

def cli_build_map():
    cfg = load_config()
    _print_json(cfg)

def cli_encode_file(path):
    cfg = load_config()
    p = Path(path)
    if not p.exists():
        print("File not found:", path); return
    text = p.read_text(errors="ignore")
    seed_vectors = build_seed_vector_from_map(cfg.get("alphabet_map", DEFAULT_MAP), cfg.get("vector_size", DEFAULT_VECTOR_SIZE))
    vec = encode_text_to_vector(text, cfg=cfg, seed_vectors=seed_vectors)
    out = {
        "file": str(p),
        "vector_size": len(vec),
        "vector_head": vec[:8],
        "entropy": shannon_entropy(text),
        "readability": readability_flesch(text)
    }
    _print_json(out)

def cli_add_to_index(item_id, path):
    p = Path(path)
    if not p.exists():
        print("File not found:", path); return
    text = p.read_text(errors="ignore")
    item = index_add_item(item_id, text)
    _print_json({"added": item_id, "snippet": item["text_snippet"]})

def cli_search(query, top=6):
    res = index_search_text(query, top_n=int(top))
    out = []
    for score, item in res:
        out.append({
            "score": score,
            "id": item.get("id"),
            "snippet": item.get("text_snippet")
        })
    _print_json({"query": query, "results": out})

# --------- Example utilities for programmatic use ----------
def build_and_save_default_config():
    cfg = load_config()
    cfg["alphabet_map"].update({k: float(v) for k,v in cfg["alphabet_map"].items()})
    save_config(cfg)
    return cfg

# --------- Module test runner ----------
if __name__ == "__main__":
    import sys, argparse
    parser = argparse.ArgumentParser(prog="alphabet_engine.py")
    sub = parser.add_subparsers(dest="cmd")

    sub.add_parser("show-config", help="Display current config")
    p_enc = sub.add_parser("encode-file", help="Encode a file and show vector head")
    p_enc.add_argument("path")
    p_add = sub.add_parser("add-to-index", help="Add file to index")
    p_add.add_argument("id")
    p_add.add_argument("path")
    p_search = sub.add_parser("search", help="Search index for query text")
    p_search.add_argument("query")
    p_search.add_argument("--top", default=6)

    args = parser.parse_args()
    if args.cmd == "show-config":
        cli_build_map()
    elif args.cmd == "encode-file":
        cli_encode_file(args.path)
    elif args.cmd == "add-to-index":
        cli_add_to_index(args.id, args.path)
    elif args.cmd == "search":
        cli_search(args.query, top=args.top)
    else:
        parser.print_help()
