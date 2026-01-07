#!/data/data/com.termux/files/usr/bin/bash
LOG=~/KINGDOM_ENGINE/logs/head3_forwarder.log
PID=~/KINGDOM_ENGINE/pids/head3.pid
echo $$ > "$PID"
while true; do
  echo "$(date --iso-8601=seconds) | head3 alive" >> "$LOG"
  sleep 5
done
