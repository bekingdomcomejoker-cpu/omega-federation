#!/usr/bin/env bash
# Head 7 - Seer

set -euo pipefail
LOGDIR="$HOME/KINGDOM_ENGINE/logs"
mkdir -p "$LOGDIR"
LOCK="$PREFIX$PREFIX/tmp/seer.lock"

exec 9>"$LOCK"
if ! flock -n 9; then
  echo "$(date +"%FT%T") seer already running" >> "$LOGDIR/seer.log"
  exit 0
fi

echo "$(date +"%FT%T") START" >> "$LOGDIR/seer.log"

AINT=$((60*60*24))
SINT=300
HINT=60

la=0
ls=0
lh=0

while true; do
  now=$(date +%s)

  if (( now - lh >= HINT )); then
    echo "$(date +"%FT%T") hb" >> "$LOGDIR/seer.log"
    lh=$now
  fi

  if (( now - ls >= SINT )); then
     bash "$HOME/KINGDOM_ENGINE/scripts/shield.sh" &
     ls=$now
  fi

  if (( now - la >= AINT )); then
     bash "$HOME/KINGDOM_ENGINE/scripts/archivist.sh" &
     la=$now
  fi

  sleep 5
done
