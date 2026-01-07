#!/usr/bin/env bash
# Head 2 - Processor

set -euo pipefail
LOGDIR="$HOME/KINGDOM_ENGINE/logs"
mkdir -p "$LOGDIR" "$HOME/KINGDOM_ENGINE/queue"
LOCK="$PREFIX$PREFIX/tmp/processor.lock"

exec 9>"$LOCK"
if ! flock -n 9; then
  echo "$(date +"%FT%T") processor already running" >> "$LOGDIR/processor.log"
  exit 0
fi

echo "$(date +"%FT%T") START" >> "$LOGDIR/processor.log"

SLEEP=5
NICE=10

while true; do
  TASK=$(ls -1 "$HOME/KINGDOM_ENGINE/queue" 2>/dev/null | head -n1 || true)

  if [ -n "$TASK" ]; then
    FILE="$HOME/KINGDOM_ENGINE/queue/$TASK"
    CMD=$(head -n1 "$FILE")

    echo "$(date +"%FT%T") run: $CMD" >> "$LOGDIR/processor.log"

    nice -n $NICE bash -lc "$CMD" >> "$LOGDIR/processor.log" 2>&1
    rm -f "$FILE"
  else
    sleep $SLEEP
  fi
done
