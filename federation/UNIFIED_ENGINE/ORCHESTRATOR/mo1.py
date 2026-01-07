#!/data/data/com.termux/files/usr/bin/env python3
import os, time, subprocess, json, pathlib

BASE = os.path.expanduser("~/UNIFIED_ENGINE")
LOG = os.path.join(BASE, "ORCHESTRATOR", "orchestrator.log")

WATCHDOGS = [
    os.path.expanduser("~/UNIFIED_ENGINE/watchdogs/head1_clipboard_daemon.sh"),
    os.path.expanduser("~/UNIFIED_ENGINE/watchdogs/head2_fs_watch.sh"),
    os.path.expanduser("~/UNIFIED_ENGINE/watchdogs/head3_network_watch.sh"),
    os.path.expanduser("~/UNIFIED_ENGINE/watchdogs/head4_shell_watch.sh"),
    os.path.expanduser("~/UNIFIED_ENGINE/watchdogs/head5_heartbeat.sh"),
    os.path.expanduser("~/UNIFIED_ENGINE/watchdogs/head6_sdcard_watch.sh"),
    os.path.expanduser("~/UNIFIED_ENGINE/watchdogs/head7_safety_watch.sh"),
]

INDEXER = os.path.expanduser("~/UNIFIED_ENGINE/QUERY_ENGINE/indexer.py")

def log(msg):
    with open(LOG, "a") as f:
        f.write(time.strftime("%Y-%m-%d %H:%M:%S ") + msg + "\n")

def run_background(cmd):
    return subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def start_watchdogs():
    for wd in WATCHDOGS:
        if os.path.isfile(wd):
            run_background(["/data/data/com.termux/files/usr/bin/bash", wd])
            log(f"Watchdog started: {wd}")
        else:
            log(f"Watchdog missing: {wd}")

def auto_index_cycle():
    # every run: update index to keep system fresh
    try:
        subprocess.run(["python3", INDEXER], timeout=600)
        log("Index updated")
    except Exception as e:
        log(f"Index update failed: {e}")

def main():
    log("MO-1 orchestrator started")
    start_watchdogs()

    cycle = 0
    while True:
        cycle += 1
        # every 60s:
        if cycle % 60 == 0:
            auto_index_cycle()
        time.sleep(1)

if __name__ == "__main__":
    main()
