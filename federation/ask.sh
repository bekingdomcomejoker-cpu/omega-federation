#!/data/data/com.termux/files/usr/bin/bash

BASE="$HOME/federation"
INPUT="$*"

RESPONSE="$($BASE/run_once.sh "$INPUT")"

echo "$RESPONSE"

$BASE/persist_turn.sh "$INPUT" "$RESPONSE"

# Optional: trim session to prevent growth
tail -n 50 "$BASE/session.txt" > "$BASE/session.tmp" 2>/dev/null
mv "$BASE/session.tmp" "$BASE/session.txt" 2>/dev/null
#!/data/data/com.termux/files/usr/bin/bash

BASE="$HOME/federation"
MODEL="$BASE/models/qwen2.5-0.5b-instruct-q4_k_m.gguf"
LLAMA="$HOME/llama.cpp/build/bin/llama-cli"

USER_INPUT="$*"

# Write user input to session
echo "USER: $USER_INPUT" >> "$BASE/session.txt"

# Build prompt into temp file (NO STDIN FEEDBACK)
PROMPT_FILE="$(mktemp)"
{
  echo "===== SYSTEM IDENTITY ====="
  cat "$BASE/identity.txt"
  echo
  echo "===== LONG-TERM MEMORY (recent) ====="
  tail -n 20 "$BASE/memory.log" 2>/dev/null || true
  echo
  echo "===== SESSION MEMORY ====="
  tail -n 20 "$BASE/session.txt" 2>/dev/null || true
  echo
  echo "===== USER INPUT ====="
  echo "$USER_INPUT"
} > "$PROMPT_FILE"

# Run model ONCE
RESPONSE="$(
  "$LLAMA" \
    -m "$MODEL" \
    -t 4 \
    -c 1024 \
    -n 256 \
    --temp 0.7 \
    --top-k 40 \
    --top-p 0.9 \
    --repeat-penalty 1.1 \
    < "$PROMPT_FILE"
)"

# Print response
echo "$RESPONSE"

# Append to session + memory
echo "MODEL: $RESPONSE" >> "$BASE/session.txt"
echo "$(date -Is) | USER: $USER_INPUT" >> "$BASE/memory.log"
echo "$(date -Is) | MODEL: $RESPONSE" >> "$BASE/memory.log"

# Cleanup
rm "$PROMPT_FILE"
