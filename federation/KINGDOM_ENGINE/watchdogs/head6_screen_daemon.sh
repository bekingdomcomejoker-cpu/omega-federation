#!/data/data/com.termux/files/usr/bin/bash
LOG=~/UNIFIED_ENGINE/logs/head6_screen.log
LAST=""

while true; do
    NEW=$(dumpsys power | grep -E "Display Power|mWakefulness" | sha256sum)
    if [ "$NEW" != "$LAST" ]; then
        echo "$(date) | SCREEN/POWER EVENT" >> "$LOG"
        LAST="$NEW"
    fi
    sleep 3
done
