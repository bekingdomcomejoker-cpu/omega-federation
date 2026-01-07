#!/data/data/com.termux/files/usr/bin/bash
LOG=~/KINGDOM_ENGINE/logs/head7_integrity.log
PID=~/KINGDOM_ENGINE/pids/head7.pid
TARGET=~/KINGDOM_ENGINE
echo $$ > "$PID"
while true; do
  echo "$(date --iso-8601=seconds) | head7 integrity scan start" >> "$LOG"
  # quick checksum summary (fast)
  find "$TARGET" -maxdepth 2 -type f -exec md5sum {} \; 2>/dev/null | wc -l >> "$LOG"
  echo "$(date --iso-8601=seconds) | head7 integrity scan done" >> "$LOG"
  sleep 30
done
