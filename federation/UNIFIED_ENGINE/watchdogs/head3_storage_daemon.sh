#!/data/data/com.termux/files/usr/bin/bash
LOG=~/UNIFIED_ENGINE/logs/head3_storage.log

while true; do
    FREE=$(df -h /data | awk 'NR==2{print $4}')
    USEP=$(df -h /data | awk 'NR==2{print $5}')
    echo "$(date) | Free: $FREE | Used: $USEP" >> "$LOG"
    sleep 60
done
