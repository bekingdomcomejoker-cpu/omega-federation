#!/data/data/com.termux/files/usr/bin/bash

BASE="$HOME/federation"
MODEL="$BASE/models/qwen2.5-0.5b-instruct-q4_k_m.gguf"

PROMPT="$(
  echo "===== SYSTEM IDENTITY ====="
  cat "$BASE/identity.txt"
  echo
  echo "===== LONG-TERM MEMORY (recent) ====="
  tail -n 20 "$BASE/memory.log" 2>/dev/null
  echo
  echo "===== SESSION MEMORY ====="
  tail -n 20 "$BASE/session.txt" 2>/dev/null
  echo
  echo "===== USER INPUT ====="
  echo "$1"
)"

echo "$PROMPT" | llama-cli \
  -m "$MODEL" \
  -c 1536 \
  -n 256 \
  --temp 0.7 \
  --top-p 0.9 \
  --repeat-penalty 1.1
