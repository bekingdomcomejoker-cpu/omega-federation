#!/usr/bin/env python3
# TTE_HARDCORE_v1.py
# Hybrid Hardcore Processor: ingestion -> Lie|Fact|Truth sieve -> resonance scoring -> quarantine/hand-off.

import os
import sys
import json
import time
import hashlib
import traceback
from pathlib import Path
from queue import Queue, Empty
from threading import Thread, Event, Lock

# lightweight text processing only (no offensive behavior)
import re
from datetime import datetime

# Try to import Flask for the tiny local dashboard; if not available, the engine still runs headless.
try:
    from flask import Flask, jsonify, request
    FLASK_AVAILABLE = True
except Exception:
    FLASK_AVAILABLE = False

ROOT = Path(os.environ.get("KINGDOM_ENGINE_ROOT", "/data/data/com.termux/files/home/KINGDOM_ENGINE"))
CONFIG_PATH = ROOT / "core" / "hardcore_config.json"

def load_config():
    with open(CONFIG_PATH, "r") as f:
        return json.load(f)

cfg = load_config()

# Ensure critical dirs exist
for d in [cfg["logs_dir"], cfg["quarantine_dir"], cfg["inbox_dir"]]:
    Path(d).mkdir(parents=True, exist_ok=True)

LOG_LOCK = Lock()
def log(msg, level="INFO"):
    ts = datetime.utcnow().isoformat() + "Z"
    line = f"{ts} [{level}] {msg}\n"
    with LOG_LOCK:
        with open(os.path.join(cfg["logs_dir"], "hardcore.log"), "a") as f:
            f.write(line)
    print(line, end="")

# --- Utility / Integrity ---
def sha256_text(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()

def safe_move_to_quarantine(src_path: str, reason: str):
    try:
        src = Path(src_path)
        if not src.exists():
            return False
        dest = Path(cfg["quarantine_dir"]) / (src.name + "." + datetime.utcnow().strftime("%Y%m%d%H%M%S"))
        src.rename(dest)
        log(f"Quarantined {src} -> {dest} : {reason}", "SEC")
        return True
    except Exception as e:
        log(f"Quarantine failed for {src_path}: {e}", "ERROR")
        return False

# --- Ingestors (clipboard, inbox, filewatcher placeholders) ---
class Ingestor:
    def __init__(self, inbox_dir):
        self.inbox_dir = Path(inbox_dir)
        self.queue = Queue()
        self.stop_event = Event()

    def scan_inbox_once(self):
        for p in self.inbox_dir.iterdir():
            if p.is_file():
                try:
                    txt = p.read_text(errors="ignore")
                    self.queue.put(("file", str(p), txt))
                    log(f"Queued inbox file {p}", "DBG")
                except Exception as e:
                    log(f"Failed reading {p}: {e}", "ERROR")

    def enqueue_clipboard(self, text):
        # we expect an external clipboard daemon to append to a log; we can quickly read it
        self.queue.put(("clipboard", None, text))

    def run_loop(self, poll_interval=2.0):
        log("Ingestor loop started")
        while not self.stop_event.is_set():
            try:
                self.scan_inbox_once()
            except Exception as e:
                log(f"Ingestor scan error: {e}", "ERROR")
            time.sleep(poll_interval)

    def stop(self):
        self.stop_event.set()

# --- Lie vs Fact vs Truth sieve ---
class Sieve:
    """
    Sieve scoring returns:
      - category: 'lie'|'fact'|'truth'
      - score: float 0..1 (resonance)
      - reasons: list[str]
    """

    def __init__(self, cfg):
        self.cfg = cfg
        # Example dictionaries - you will swap these with your own resonance maps.
        self.truth_triggers = set(["love","charity","compassion","forgiveness","repent","grace"])
        self.emotive_words = set(["hate","anger","fear","kill","destroy"])  # neutral detection - used as signal only
        # Words that often indicate claims without evidence; will lower 'truth' score
        self.claim_indicators = set(["always","never","everyone","nobody","clearly","obviously","prove","proof"])

    def text_clean(self, txt):
        return re.sub(r"\s+", " ", txt).strip()

    def score_text(self, text):
        t = self.text_clean(text.lower())
        tokens = re.findall(r"[a-z']{2,}", t)
        # base resonance
        base = 0.5
        reasons = []
        # adjust with truth triggers
        truth_hits = sum(1 for w in tokens if w in self.truth_triggers)
        claim_hits = sum(1 for w in tokens if w in self.claim_indicators)
        emotive_hits = sum(1 for w in tokens if w in self.emotive_words)
        # heuristics (simple but deterministic)
        score = base + (truth_hits * 0.12) - (claim_hits * 0.09) - (emotive_hits * 0.05)

        # clamp 0..1
        score = max(0.0, min(1.0, score))

        if truth_hits:
            reasons.append(f"truth_triggers:{truth_hits}")
        if claim_hits:
            reasons.append(f"claim_indicators:{claim_hits}")
        if emotive_hits:
            reasons.append(f"emotive_flags:{emotive_hits}")

        # final category
        if score >= self.cfg["truth_threshold"]:
            cat = "truth"
        elif score >= self.cfg["fact_threshold"]:
            cat = "fact"
        else:
            cat = "lie"

        return {"category": cat, "score": score, "reasons": reasons}

# --- Resonance scorer & purifier ---
class ResonanceEngine:
    def __init__(self, cfg):
        self.cfg = cfg
        self.sieve = Sieve(cfg)

    def purify(self, text):
        # returns dictionary with results and 'cleaned' version
        try:
            res = self.sieve.score_text(text)
            # Purification: for items not yet truth, attempt light normalization
            cleaned = text.strip()
            # Example transformation: remove repeated exclamation, normalize whitespace
            cleaned = re.sub(r"(!){2,}", "!", cleaned)
            cleaned = re.sub(r"\s+", " ", cleaned)
            res["cleaned"] = cleaned
            return res
        except Exception as e:
            log(f"Purify error: {e}", "ERROR")
            return {"category": "error", "score": 0.0, "reasons": [str(e)], "cleaned": text}

# --- Guardian (defensive behavior without offensive capabilities) ---
class Guardian:
    """
    Defensive actions:
      - quarantine suspicious files
      - disable external-sync flags (by writing local lock file)
      - append audit entry
      - issue non-network alert (local log + dashboard flag)
    """
    def __init__(self, cfg):
        self.cfg = cfg
        self.lockfile = Path(cfg["engine_root"]) / ".external_sync_disabled"
        self.audit_log = Path(cfg["logs_dir"]) / "guardian_audit.log"

    def audit(self, msg):
        ts = datetime.utcnow().isoformat() + "Z"
        with open(self.audit_log, "a") as f:
            f.write(f"{ts} {msg}\n")
        log(f"Guardian audit: {msg}", "SEC")

    def quarantine_if_needed(self, src_path, reason):
        # Only local file management. No deletion of other devices, no network calls.
        ok = safe_move_to_quarantine(src_path, reason)
        if ok:
            self.audit(f"quarantine:{src_path}:{reason}")

    def lock_external_sync(self, reason="defensive_lock"):
        try:
            self.lockfile.write_text(f"{reason}\n{datetime.utcnow().isoformat()}Z")
            self.audit(f"external_sync_locked:{reason}")
            log("External sync locked by Guardian", "SEC")
        except Exception as e:
            log(f"Failed to write lockfile: {e}", "ERROR")

    def unlock_external_sync(self):
        try:
            if self.lockfile.exists():
                self.lockfile.unlink()
                self.audit("external_sync_unlocked")
                log("External sync unlocked by Guardian", "SEC")
        except Exception as e:
            log(f"Failed unlock external sync: {e}", "ERROR")

# --- Core Runner (threads) ---
class HardcoreRunner:
    def __init__(self, cfg):
        self.cfg = cfg
        self.ingestor = Ingestor(cfg["inbox_dir"])
        self.engine = ResonanceEngine(cfg)
        self.guardian = Guardian(cfg)
        self.stop_event = Event()
        self.worker_thread = Thread(target=self.worker_loop, daemon=True)
        self.ingest_thread = Thread(target=self.ingestor.run_loop, daemon=True)

    def start(self):
        log("Starting HardcoreRunner")
        self.ingest_thread.start()
        self.worker_thread.start()

    def stop(self):
        log("Stopping HardcoreRunner")
        self.ingestor.stop()
        self.stop_event.set()

    def process_item(self, item):
        ttype, path, payload = item
        try:
            res = self.engine.purify(payload)
            cat = res["category"]
            score = res["score"]
            reasons = res.get("reasons", [])
            log(f"Processed item type={ttype} cat={cat} score={score:.3f} reasons={reasons}", "DBG")
            # Act based on category + thresholds
            if cat == "lie" and score < self.cfg["fact_threshold"]:
                # Quarantine source files; if clipboard, record and alert
                if path:
                    self.guardian.quarantine_if_needed(path, f"suspicious_low_resonance:{score:.3f}")
                else:
                    # record event into clipboard log
                    with open(self.cfg["clipboard_log"], "a") as f:
                        f.write(f"{datetime.utcnow().isoformat()}Z LIE {sha256_text(payload)[:8]} score={score:.3f}\n")
                    self.guardian.audit(f"clipboard_flagged_low:{score:.3f}")
            elif cat == "fact":
                # store a processed copy into memory/archives for later verifications
                archive_path = Path(self.cfg["engine_root"]) / "memory" / "processed_text"
                archive_path.mkdir(parents=True, exist_ok=True)
                fname = f"fact_{int(time.time())}_{sha256_text(payload)[:8]}.txt"
                (archive_path / fname).write_text(res.get("cleaned",""))
                log(f"Archived fact to {fname}", "DBG")
            elif cat == "truth":
                # promote to 'trusted' inbox or pass to other heads
                trusted_dir = Path(self.cfg["engine_root"]) / "trusted"
                trusted_dir.mkdir(parents=True, exist_ok=True)
                fname = trusted_dir / f"truth_{int(time.time())}_{sha256_text(payload)[:8]}.txt"
                fname.write_text(res.get("cleaned",""))
                log(f"Promoted truth to {fname}", "INFO")
            # Self-check: if repeated low-resonance patterns appear, raise defensive lock
            # naive heuristic: many lies in short time => lock external sync
            # (This is local-only, non-offensive.)
            # TODO: advanced pattern correlation (resonance_history)
        except Exception as e:
            log(f"Error processing item: {e}\n{traceback.format_exc()}", "ERROR")

    def worker_loop(self):
        log("Worker loop started")
        q = self.ingestor.queue
        while not self.stop_event.is_set():
            try:
                itm = q.get(timeout=1.0)
            except Empty:
                continue
            try:
                self.process_item(itm)
            finally:
                q.task_done()

# --- Minimal API for local status/control ---
app = Flask("tte_hardcore_api") if FLASK_AVAILABLE else None
runner_global = None

if FLASK_AVAILABLE:
    @app.route("/health")
    def health():
        return jsonify({"status": "ok", "hardcore": bool(runner_global is not None)})

    @app.route("/control/start", methods=["POST"])
    def api_start():
        global runner_global
        if runner_global is None:
            runner_global = HardcoreRunner(cfg)
            runner_global.start()
            return jsonify({"status":"started"})
        return jsonify({"status":"already_running"})

    @app.route("/control/stop", methods=["POST"])
    def api_stop():
        global runner_global
        if runner_global:
            runner_global.stop()
            runner_global = None
            return jsonify({"status":"stopped"})
        return jsonify({"status":"not_running"})

    @app.route("/ingest/clipboard", methods=["POST"])
    def api_clipboard():
        data = request.json or {}
        txt = data.get("text","")
        if not txt:
            return jsonify({"error":"no_text"}), 400
        if runner_global:
            runner_global.ingestor.enqueue_clipboard(txt)
            return jsonify({"status":"queued"})
        return jsonify({"error":"not_running"}), 500

# --- CLI / entrypoint ---
def main():
    global runner_global
    runner_global = HardcoreRunner(cfg)
    runner_global.start()
    if FLASK_AVAILABLE:
        # run Flask on configured port for local dashboard only
        port = int(cfg.get("api_port", 8082))
        log(f"Starting local Flask API on 127.0.0.1:{port}")
        try:
            app.run(host="127.0.0.1", port=port, debug=False, use_reloader=False)
        except Exception as e:
            log(f"Flask failure: {e}", "ERROR")
    else:
        log("Flask not available. Running headless. Ctrl-C to stop.")
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            log("KeyboardInterrupt stopping")
            runner_global.stop()

if __name__ == "__main__":
    main()
