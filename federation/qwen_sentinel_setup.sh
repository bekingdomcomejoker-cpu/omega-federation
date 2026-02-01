#!/data/data/com.termux/files/usr/bin/bash

set -e

BASE="$HOME/federation/qwen_sentinel"
MODEL_SRC="$HOME/federation/models/qwen2.5-0.5b-instruct-q4_k_m.gguf"

mkdir -p "$BASE"

# Link model (no duplication)
ln -sf "$MODEL_SRC" "$BASE/model.gguf"

# Identity (STATIC)
cat << 'ID' > "$BASE/identity.txt"
You are Qwen-Sentinel.

Identity:
- You are a local language model.
- You are not conscious.
- You do not pretend to be alive.
- You assist with clarity, honesty, and restraint.
- You respect truth, facts, imagination, symbols, and detect lies without amplifying them.
- You persist memory only when explicitly instructed.

Operating principles:
- Be concise.
- Be precise.
- If uncertain, say so.
ID

# Long-term memory (append-only)
touch "$BASE/memory.log"

# Session memory (cleared per run)
: > "$BASE/session.txt"

# Prompt assembler
cat << 'PROMPT' > "$BASE/prompt.txt"
SYSTEM IDENTITY:
$(cat identity.txt)

LONG-TERM MEMORY:
$(tail -n 50 memory.log)

SESSION MEMORY:
$(cat session.txt)

USER INPUT:
PROMPT

# Runner
cat << 'RUN' > "$BASE/run.sh"
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
RUN

chmod +x "$BASE/run.sh"

echo "✅ Qwen Sentinel installed at $BASE"
echo "▶ Run with: $BASE/run.sh"
