#!/bin/bash
# WIRE — Primary Reasoning with Deterministic Context Rehydration (stdout-safe)

export LD_LIBRARY_PATH="$HOME/federation/KINGDOM_ENGINE/models/llama_cpp/build/bin:$LD_LIBRARY_PATH"

LLAMA_BIN="$HOME/federation/KINGDOM_ENGINE/models/llama_cpp/build/bin/llama-cli"
MODEL="$HOME/llama.cpp/models/qwen1_5-1_8b-chat-q4_k_m.gguf"

INPUT="$*"

SOUL_CONTEXT=$(python3 ~/federation_memory_bridge.py)

RAW_OUTPUT=$(
  "$LLAMA_BIN" \
    -m "$MODEL" \
    -p "SYSTEM CONTEXT:
$SOUL_CONTEXT

USER QUESTION:
$INPUT

FINAL ANSWER:" \
    --temp 0.1 \
    -n 256 \
    --log-disable \
    </dev/null
)

# Force flush & visibility
echo "$RAW_OUTPUT"
