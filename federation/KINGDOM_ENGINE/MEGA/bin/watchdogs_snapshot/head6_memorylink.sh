#!/data/data/com.termux/files/usr/bin/bash
LOG=~/KINGDOM_ENGINE/logs/head6_memorylink.log
PID=~/KINGDOM_ENGINE/pids/head6.pid
echo $$ > "$PID"
while true; do
  echo "$(date --iso-8601=seconds) | head6 memory heartbeat" >> "$LOG"
  sleep 10
done
