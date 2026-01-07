#!/data/data/com.termux/files/usr/bin/bash
INBOX="$HOME/KINGDOM_ENGINE/MEGA/inbox/head3"
LOG="$HOME/KINGDOM_ENGINE/MEGA/logs/head3_inbox.log"

mkdir -p "$INBOX"

process_inbox() {
    for msg in "$INBOX"/*; do
        [ -f "$msg" ] || continue
        payload=$(cat "$msg")
        echo "$(date -Iseconds) [head3] RECEIVED: $payload" >> "$LOG"
        rm -f "$msg"
    done
}

while true; do
    sleep 0.3
    process_inbox
done
