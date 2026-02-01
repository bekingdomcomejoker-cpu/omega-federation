#!/data/data/com.termux/files/usr/bin/bash

BASE="$(cd "$(dirname "$0")" && pwd)"
MODEL="$BASE/model.gguf"

read -r -p "You: " USER_INPUT

echo "$USER_INPUT" >> "$BASE/session.txt"

PROMPT=$(sed "s|USER INPUT:|USER INPUT:\n$USER_INPUT|" "$BASE/prompt.txt")

llama-cli \
  -m "$MODEL" \
  -c 2048 \
  -n 256 \
  --temp 0.7 \
  --repeat_penalty 1.1 \
  -p "$PROMPT"
