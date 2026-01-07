#!/data/data/com.termux/files/usr/bin/bash
# head9.sh - wrapper to manage head9 (Missionary)
REAL="$HOME/KINGDOM_ENGINE/watchdogs/head9_missionary_daemon.sh"
LOG="$HOME/KINGDOM_ENGINE/logs/head9_wrapper.log"
PIDFILE="$HOME/KINGDOM_ENGINE/MEGA/run/head9.pid"

mkdir -p "$(dirname "$PIDFILE")" "$(dirname "$LOG")"

# If an old PID exists and process is alive, exit (prevent double-start)
if [ -f "$PIDFILE" ]; then
  oldpid=$(cat "$PIDFILE" 2>/dev/null)
  if [ -n "$oldpid" ] && kill -0 "$oldpid" 2>/dev/null; then
    echo "Head9 already running (PID $oldpid)" >> "$LOG"
    exit 0
  else
    rm -f "$PIDFILE"
  fi
fi

# Verify target exists
if [ ! -x "$REAL" ]; then
  echo "ERROR: target daemon not found or not executable: $REAL" >> "$LOG"
  exit 2
fi

# Start the daemon in background and capture PID
nohup bash "$REAL" >> "$LOG" 2>&1 &
echo $! > "$PIDFILE"
echo "Started head9 (PID $(cat "$PIDFILE")) at $(date --iso-8601=seconds)" >> "$LOG"

# Optional: keep wrapper process alive to mirror behavior (exit is also fine)
exit 0
