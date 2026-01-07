#!/data/data/com.termux/files/usr/bin/bash
LOG=~/UNIFIED_ENGINE/logs/head1_clipboard.log
LAST=""

while true; do
    NEW=$(termux-clipboard-get 2>/dev/null)
    if [ "$NEW" != "$LAST" ]; then
        echo "$(date) | CLIPBOARD: $NEW" >> "$LOG"
        LAST="$NEW"
    fi
    sleep 1
done
