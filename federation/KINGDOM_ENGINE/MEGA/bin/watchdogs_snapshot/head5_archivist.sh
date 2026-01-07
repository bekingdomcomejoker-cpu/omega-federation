#!/bin/bash
WATCH=~/KINGDOM_ENGINE
BACKUP=~/KINGDOM_ENGINE/immutable_backups
LOG=~/KINGDOM_ENGINE/logs/head5_archivist.log

mkdir -p "$BACKUP"

while true; do
    SNAP="$BACKUP/snap_$(date +%s)"
    mkdir -p "$SNAP"
    rsync -a --exclude="immutable_backups" "$WATCH/" "$SNAP/"
    echo "[OK] Snapshot $SNAP" >> "$LOG"
    sleep 600
done
