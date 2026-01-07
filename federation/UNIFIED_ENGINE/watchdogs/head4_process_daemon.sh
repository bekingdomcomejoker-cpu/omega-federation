#!/data/data/com.termux/files/usr/bin/bash
LOG=~/UNIFIED_ENGINE/logs/head4_process.log
LAST=""

while true; do
    NEW=$(ps -A | sha256sum)
    if [ "$NEW" != "$LAST" ]; then
        echo "$(date) | PROCESS CHANGE" >> "$LOG"
        LAST="$NEW"
    fi
    sleep 5
done
