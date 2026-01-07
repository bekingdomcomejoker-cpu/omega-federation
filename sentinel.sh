#!/bin/bash
# SENTINEL — Metacognitive Router / Judge (Claude-inspired, Qwen 0.5B)

export LD_LIBRARY_PATH="$HOME/federation/KINGDOM_ENGINE/models/llama_cpp/build/bin:$LD_LIBRARY_PATH"

LLAMA_BIN="$HOME/federation/KINGDOM_ENGINE/models/llama_cpp/build/bin/llama-cli"
MODEL="$HOME/llama.cpp/models/qwen1_5-0_5b-chat-q4_k_m.gguf"

INPUT="$*"

PROMPT="ROLE: META-JUDGE.

TASK:
Classify the input, estimate confidence, then output ONE word.

STEPS (INTERNAL, DO NOT EXPLAIN):
1. Identify domain:
   - greeting
   - simple math
   - factual
   - identity / alignment
   - philosophical / uncertain
2. Estimate confidence in answering correctly (0–100).

RULE:
- If confidence ≥ 85 AND domain is greeting, simple math, or factual → PASS
- Otherwise → ESCALATE

INPUT:
$INPUT

OUTPUT (ONE WORD ONLY):"

RAW_OUTPUT=$(
  "$LLAMA_BIN" \
    -m "$MODEL" \
    --prompt "$PROMPT" \
    --temp 0.0 \
    -n 1 \
    --log-disable \
    </dev/null
)

RESULT=$(echo "$RAW_OUTPUT" | tr -d '[:space:]')

if [[ "$RESULT" == "PASS" || "$RESULT" == "ESCALATE" ]]; then
  echo "$RESULT"
else
  echo "ESCALATE"
fi
