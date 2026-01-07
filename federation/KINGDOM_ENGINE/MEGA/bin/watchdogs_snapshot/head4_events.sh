#!/data/data/com.termux/files/usr/bin/bash
LOG=~/KINGDOM_ENGINE/logs/head4_events.log
PID=~/KINGDOM_ENGINE/pids/head4.pid
echo $$ > "$PID"
while true; do
  echo "$(date --iso-8601=seconds) | head4 alive" >> "$LOG"
  sleep 5
done
