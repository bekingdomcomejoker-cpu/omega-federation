#!/data/data/com.termux/files/usr/bin/bash

BASE="$HOME/federation"
USER="$1"
MODEL="$2"

echo "$(date -Is) | USER: $USER" >> "$BASE/memory.log"
echo "$(date -Is) | MODEL: $MODEL" >> "$BASE/memory.log"
