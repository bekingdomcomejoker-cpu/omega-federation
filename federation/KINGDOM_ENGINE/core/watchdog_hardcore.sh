#!/usr/bin/env bash
ROOT="/data/data/com.termux/files/home/KINGDOM_ENGINE"
PIDFILE="$ROOT/core/hardcore.pid"
while true; do
  if [ -f "$PIDFILE" ]; then
    PID=\$(cat "$PIDFILE")
    if ! kill -0 \$PID > /dev/null 2>&1; then
      echo "Process \$PID not running, restarting..."
      bash "$ROOT/core/start_hardcore.sh"
    fi
  else
    echo "No pidfile, starting hardcore"
    bash "$ROOT/core/start_hardcore.sh"
  fi
  sleep 10
done
