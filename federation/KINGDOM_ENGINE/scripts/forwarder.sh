#!/usr/bin/env bash
# Head 3 - Forwarder

set -euo pipefail
LOGDIR="$HOME/KINGDOM_ENGINE/logs"
mkdir -p "$LOGDIR"
LOCK="$PREFIX$PREFIX/tmp/forwarder.lock"

exec 9>"$LOCK"
if ! flock -n 9; then
  echo "$(date +"%FT%T") forwarder already running" >> "$LOGDIR/forwarder.log"
  exit 0
fi

echo "$(date +"%FT%T") START" >> "$LOGDIR/forwarder.log"

PING="8.8.8.8"
INT=30

while true; do
  if ping -c1 -W2 "$PING" >/dev/null 2>&1; then
    echo "$(date +"%FT%T") OK" >> "$LOGDIR/forwarder.log"
  else
    echo "$(date +"%FT%T") DOWN" >> "$LOGDIR/forwarder.log"
  fi
  sleep $INT
done
