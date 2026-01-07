#!/usr/bin/env bash
# Head 1 - Clipboard Daemon

set -euo pipefail
LOGDIR="$HOME/KINGDOM_ENGINE/logs"
mkdir -p "$LOGDIR" "$HOME/KINGDOM_ENGINE/inbox"
LOCKFILE="$PREFIX$PREFIX/tmp/clipboard_daemon.lock"

exec 9>"$LOCKFILE"
if ! flock -n 9; then
  echo "$(date +"%FT%T") already running" >> "$LOGDIR/clipboard_daemon.log"
  exit 0
fi

echo "$(date +"%FT%T") START" >> "$LOGDIR/clipboard_daemon.log"

INTERVAL=3
LAST=""

while true; do
  CLIP=$(termux-clipboard-get 2>/dev/null || true)

  if [ -n "$CLIP" ] && [ "$CLIP" != "$LAST" ]; then
    TS=$(date +"%Y%m%d_%H%M%S")
    OUT="$HOME/KINGDOM_ENGINE/inbox/clip_$TS.txt"
    echo "$CLIP" > "$OUT"
    echo "$(date +"%FT%T") saved $OUT" >> "$LOGDIR/clipboard_daemon.log"
    LAST="$CLIP"
  fi

  sleep $INTERVAL
done
