#!/data/data/com.termux/files/usr/bin/bash

ROOT=~/UNIFIED_ENGINE
MIN=50000    # files larger than 50KB

find "$ROOT" -type f \
  \( -iname "*.txt" -o -iname "*.json" -o -iname "*.log" \) \
  -size +${MIN}c | while read -r f; do

    gzip -9 "$f"
done
