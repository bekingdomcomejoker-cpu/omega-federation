#!/data/data/com.termux/files/usr/bin/bash
LOG=~/KINGDOM_ENGINE/logs/head1_clipboard.log
PID=~/KINGDOM_ENGINE/pids/head1.pid
echo $$ > "$PID"
LAST=""
while true; do
  NEW=$(termux-clipboard-get 2>/dev/null || true)
  if [ "$NEW" != "$LAST" ]; then
    echo "$(date --iso-8601=seconds) | CLIPBOARD CHANGE: ${NEW:0:200}" >> "$LOG"
    LAST="$NEW"
  fi
  sleep 1
done
