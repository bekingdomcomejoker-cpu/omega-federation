#!/usr/bin/env bash
# Head 6 - Shield

set -euo pipefail
LOGDIR="$HOME/KINGDOM_ENGINE/logs"
mkdir -p "$LOGDIR"
LOCK="$PREFIX$PREFIX/tmp/shield.lock"

exec 9>"$LOCK"
if ! flock -n 9; then
  echo "$(date +"%FT%T") shield already running" >> "$LOGDIR/shield.log"
  exit 0
fi

echo "$(date +"%FT%T") START" >> "$LOGDIR/shield.log"

THRESH=10
INT=30

while true; do
  DF=$(df -P /data | tail -n1)
  USE=$(echo "$DF" | awk '{print $5}' | tr -d '%')
  FREE=$((100 - USE))

  echo "$(date +"%FT%T") free $FREE%" >> "$LOGDIR/shield.log"

  if (( FREE <= THRESH )); then
    echo "$(date +"%FT%T") cleanup" >> "$LOGDIR/shield.log"
  fi

  sleep $INT
done
