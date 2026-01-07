#!/bin/bash
WATCH=~/KINGDOM_ENGINE
BACKUP=~/KINGDOM_ENGINE/immutable_backups
LOG=~/KINGDOM_ENGINE/logs/head6_shield.log

while true; do
    for f in $(find "$WATCH" -type f); do
        REL=${f#$WATCH}
        if [ ! -f "$BACKUP/latest$REL" ]; then
            echo "[REBUILD] Restoring missing $f" >> "$LOG"
            cp "$BACKUP/latest$REL" "$f"
        fi
    done
    sleep 300
done
