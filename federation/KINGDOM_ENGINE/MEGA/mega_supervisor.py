#!/data/data/com.termux/files/usr/bin/python

import os, time, json, subprocess, signal

BASE = os.path.expanduser("~/KINGDOM_ENGINE")
MEGA = f"{BASE}/MEGA"
RUN = f"{MEGA}/run"
LOGS = f"{MEGA}/logs"
CONFIG = f"{MEGA}/mega_engine_config.json"

def load_config():
    with open(CONFIG, "r") as f:
        return json.load(f)

def start_head(path, name):
    pidfile = f"{RUN}/{name}.pid"
    logfile = f"{LOGS}/{name}.log"

    # skip if running
    if os.path.isfile(pidfile):
        try:
            pid = int(open(pidfile).read().strip())
            os.kill(pid, 0)
            return
        except:
            pass

    with open(logfile, "a") as lf:
        p = subprocess.Popen(["/data/data/com.termux/files/usr/bin/bash", path],
                             stdout=lf, stderr=lf)
        with open(pidfile, "w") as pf:
            pf.write(str(p.pid))

def monitor(config):
    heads = config["canonical_heads"]
    while True:
        for head in heads:
            name = head.replace(".sh", "")
            full = f"{BASE}/watchdogs/{head}"
            start_head(full, name)
        time.sleep(config["supervisor"]["check_interval_sec"])

if __name__ == "__main__":
    cfg = load_config()
    monitor(cfg)
