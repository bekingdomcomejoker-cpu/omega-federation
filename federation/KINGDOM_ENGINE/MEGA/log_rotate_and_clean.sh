#!/data/data/com.termux/files/usr/bin/bash

MEGA="$HOME/KINGDOM_ENGINE/MEGA"
LOGDIR="$MEGA/logs"
TMPDIR="$MEGA/tmp"

# ROTATE > 50 MB
find "$LOGDIR" -type f -size +50M -print0 | while IFS= read -r -d '' f; do
    mv "$f" "$f.$(date +%s).rot"
done

# DELETE rotated > 14 days
find "$LOGDIR" -type f -name "*.rot" -mtime +14 -delete

# CLEAN temp files > 48 hours
find "$TMPDIR" -type f -mtime +2 -delete
