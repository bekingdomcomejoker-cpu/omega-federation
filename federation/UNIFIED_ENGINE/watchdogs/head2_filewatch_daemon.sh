#!/data/data/com.termux/files/usr/bin/bash
WATCH=~/UNIFIED_ENGINE
LOG=~/UNIFIED_ENGINE/logs/head2_filewatch.log
HASH=""

while true; do
    NEW=$(find "$WATCH" -type f -exec md5sum {} \; | sha256sum)
    if [ "$NEW" != "$HASH" ]; then
        echo "$(date) | FILE CHANGE DETECTED" >> "$LOG"
        HASH="$NEW"
    fi
    sleep 3
done
