#!/data/data/com.termux/files/usr/bin/bash
TARGET=~/UNIFIED_ENGINE
LOG=~/UNIFIED_ENGINE/logs/head7_integrity.log
LAST=""

while true; do
    NEW=$(find "$TARGET" -type f -exec sha256sum {} \; | sort | sha256sum)
    if [ "$NEW" != "$LAST" ]; then
        echo "$(date) | ENGINE INTEGRITY SHIFT" >> "$LOG"
        LAST="$NEW"
    fi
    sleep 10
done
