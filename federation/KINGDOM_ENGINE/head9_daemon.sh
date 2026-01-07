#!/usr/bin/env bash
# head9_daemon.sh - Launch Head9 Missionary as a background listener
ENGINE_ROOT="$HOME/KINGDOM_ENGINE"
PY="$ENGINE_ROOT/head9_missionary.py"
LOG="$ENGINE_ROOT/logs/head9_daemon.log"
PIDFILE="$ENGINE_ROOT/pids/head9.pid"
FIFO="$ENGINE_ROOT/MEGA/inbox/head9_pipe"

mkdir -p "$(dirname "$LOG")" "$(dirname "$PIDFILE")" "$(dirname "$FIFO")"
# create FIFO if not exists
[ -p "$FIFO" ] || mkfifo "$FIFO"

# background loop: read lines from FIFO and call python script
nohup bash -c '
  echo "[$(date --iso-8601=seconds)] HEAD9 DAEMON STARTING" >> "'"$LOG"'"
  while true; do
    if read line < "'"$FIFO"'"; then
      if [ -n "$line" ]; then
        echo "$line" | python3 "'"$PY"'" >> "'"$LOG"'" 2>&1
      fi
    else
      sleep 0.5
    fi
  done
' >/dev/null 2>&1 &

echo $! > "$PIDFILE"
echo "started head9_daemon (pid $(cat $PIDFILE))" >> "$LOG"
echo "HEAD9_STARTED"
