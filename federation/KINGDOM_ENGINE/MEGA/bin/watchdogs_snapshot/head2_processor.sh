#!/data/data/com.termux/files/usr/bin/bash
LOG=~/KINGDOM_ENGINE/logs/head2_processor.log
PID=~/KINGDOM_ENGINE/pids/head2.pid
echo $$ > "$PID"
while true; do
  echo "$(date --iso-8601=seconds) | head2 alive" >> "$LOG"
  # Placeholder: replace the line below with your real start command for the processor
  # /data/data/com.termux/files/home/start_ai.sh
  sleep 5
done
