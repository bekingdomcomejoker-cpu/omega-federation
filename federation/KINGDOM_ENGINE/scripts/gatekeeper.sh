#!/usr/bin/env bash
# Head 4 - Gatekeeper

set -euo pipefail
LOGDIR="$HOME/KINGDOM_ENGINE/logs"
PIDDIR="$HOME/KINGDOM_ENGINE/pids"
mkdir -p "$LOGDIR" "$PIDDIR"
LOCK="$PREFIX$PREFIX/tmp/gatekeeper.lock"

exec 9>"$LOCK"
if ! flock -n 9; then
  echo "$(date +"%FT%T") gatekeeper already running" >> "$LOGDIR/gatekeeper.log"
  exit 0
fi

echo "$(date +"%FT%T") START" >> "$LOGDIR/gatekeeper.log"

SERVICES=(
  "clipboard|$HOME/KINGDOM_ENGINE/scripts/clipboard_daemon.sh|$PIDDIR/clipboard.pid"
  "processor|$HOME/KINGDOM_ENGINE/scripts/processor.sh|$PIDDIR/processor.pid"
  "forwarder|$HOME/KINGDOM_ENGINE/scripts/forwarder.sh|$PIDDIR/forwarder.pid"
)

start_svc() {
  local name="$1" cmd="$2" pidfile="$3"
  nohup bash "$cmd" >> "$LOGDIR/${name}.log" 2>&1 &
  echo $! > "$pidfile"
  echo "$(date +"%FT%T") started $name" >> "$LOGDIR/gatekeeper.log"
}

while true; do
  for svc in "${SERVICES[@]}"; do
    IFS='|' read -r name cmd pidfile <<< "$svc"

    if [ -f "$pidfile" ]; then
       pid=$(cat "$pidfile")
       if ! kill -0 "$pid" 2>/dev/null; then
          start_svc "$name" "$cmd" "$pidfile"
       fi
    else
       start_svc "$name" "$cmd" "$pidfile"
    fi
  done
  sleep 8
done
