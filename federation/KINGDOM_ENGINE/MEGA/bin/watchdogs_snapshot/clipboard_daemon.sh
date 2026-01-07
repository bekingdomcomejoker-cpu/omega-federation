#!/data/data/com.termux/files/usr/bin/bash

LOG_DIR="$HOME/KINGDOM_ENGINE/logs"
LAST_CLIP_HASH=""

while true; do
    CLIP_CONTENT=$(termux-clipboard-get 2>/dev/null)

    # if clipboard empty, skip
    if [ -z "$CLIP_CONTENT" ]; then
        sleep 10
        continue
    fi

    # hash clipboard
    CURRENT_HASH=$(echo -n "$CLIP_CONTENT" | sha256sum | awk '{print $1}')

    # skip if same as last capture
    if [ "$CURRENT_HASH" == "$LAST_CLIP_HASH" ]; then
        sleep 10
        continue
    fi

    # update last hash
    LAST_CLIP_HASH="$CURRENT_HASH"

    # log it
    TIMESTAMP=$(date +"%Y-%m-%d %H:%M:%S")
    echo -e "[$TIMESTAMP]\n$CLIP_CONTENT\n---" >> "$LOG_DIR/clipboard.log"

done
