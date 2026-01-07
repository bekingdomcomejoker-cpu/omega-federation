#!/data/data/com.termux/files/usr/bin/bash
LOG=~/KINGDOM_ENGINE/logs/head5_filewatch.log
PID=~/KINGDOM_ENGINE/pids/head5.pid
WATCH=~/KINGDOM_ENGINE
echo $$ > "$PID"
snap="/tmp/kingdom_snap.$$"
ls -lR "$WATCH" > "$snap"
while true; do
  tmp="/tmp/kingdom_snap2.$$"
  ls -lR "$WATCH" > "$tmp"
  if ! cmp -s "$snap" "$tmp"; then
    echo "$(date --iso-8601=seconds) | filewatch detected change" >> "$LOG"
    mv "$tmp" "$snap"
  else
    rm -f "$tmp"
  fi
  sleep 6
done
