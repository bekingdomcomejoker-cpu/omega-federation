#!/data/data/com.termux/files/usr/bin/bash

LOG=~/UNIFIED_ENGINE/logs/optimizer_daemon.log

echo "$(date) START OPTIMIZER" >> "$LOG"

python ~/UNIFIED_ENGINE/OPTIMIZER/dedupe.py >> "$LOG" 2>&1
bash ~/UNIFIED_ENGINE/OPTIMIZER/shrink_texts.sh >> "$LOG" 2>&1
bash ~/UNIFIED_ENGINE/OPTIMIZER/compress_large.sh >> "$LOG" 2>&1

echo "$(date) OPTIMIZER DONE" >> "$LOG"
