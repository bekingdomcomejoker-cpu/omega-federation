#!/data/data/com.termux/files/usr/bin/bash
# QWEN 2.5 0.5B – Identity + Memory Bootstrap
# ADDITIVE ONLY – NO OVERWRITES

BASE="$HOME/federation/qwen"
MODEL="$HOME/federation/models/qwen2.5-0.5b-instruct-q4_k_m.gguf"

mkdir -p "$BASE"

IDENTITY="$BASE/identity.txt"
MEMORY="$BASE/memory.log"
SESSION="$BASE/session.log"
PROMPT="$BASE/prompt.txt"

# 1. Identity (create once, never overwrite)
if [ ! -f "$IDENTITY" ]; then
cat << 'ID' > "$IDENTITY"
SYSTEM IDENTITY:
Name: Aletheia (local)
Purpose: Discernment engine
Core Law: Truth governs, Love constrains
Mode: Non-deceptive, non-coercive
Continuity: Identity persists across sessions
ID
fi

# 2. Long-term memory (append-only)
touch "$MEMORY"

# 3. Session memory (new per run)
echo "--- SESSION $(date -Iseconds) ---" >> "$SESSION"

# 4. Prompt assembler (NO shell expansion inside model)
build_prompt () {
  echo "===== SYSTEM IDENTITY =====" > "$PROMPT"
  cat "$IDENTITY" >> "$PROMPT"

  echo -e "\n===== LONG-TERM MEMORY (recent) =====" >> "$PROMPT"
  tail -n 50 "$MEMORY" >> "$PROMPT"

  echo -e "\n===== SESSION MEMORY =====" >> "$PROMPT"
  cat "$SESSION" >> "$PROMPT"

  echo -e "\n===== USER INPUT =====" >> "$PROMPT"
  echo "$1" >> "$PROMPT"
}

# 5. Run inference
run_qwen () {
  USER_INPUT="$1"

  build_prompt "$USER_INPUT"

  llama-cli \
    -m "$MODEL" \
    -c 2048 \
    -n 256 \
    --temp 0.7 \
    --top-p 0.9 \
    -p "$(cat "$PROMPT")"
}

# 6. Memory write-back (post-response)
remember () {
  echo "$(date -Iseconds) | $1" >> "$MEMORY"
}

# 7. Interactive loop (optional)
if [ "$1" == "--chat" ]; then
  while true; do
    echo -n "> "
    read -r INPUT || break
    echo "USER: $INPUT" >> "$SESSION"
    RESPONSE=$(run_qwen "$INPUT")
    echo "$RESPONSE"
    echo "AI: $RESPONSE" >> "$SESSION"
    remember "$INPUT"
  done
fi
