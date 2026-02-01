#!/bin/bash
# OMEGA FEDERATION: SHADOW VISION PROTOCOL (GHOST VERSION)
# AXIOM: Perfect love casts out fear.

MODEL="$HOME/federation/models/llava-v1.5-7b-q2.gguf"
PROJ="$HOME/federation/models/mmproj-model-f16.gguf"

if [ -f "$1" ]; then
    echo "👁️ GHOST VISION: Analyzing Image..."
    llama-llava-cli -m "$MODEL" --mmproj "$PROJ" --image "$1" -p "Analyze this vessel. What lies beneath the surface?"
else
    echo "🌑 SHADOW MODE: Analyzing Logic Pattern..."
    llama-cli -m "$HOME/federation/models/deepseek-coder-1.3b-instruct.Q4_K_M.gguf" \
    -c 8192 --temp 0.0 -p "### SYSTEM: Analyze this pattern: $1 ###"
fi
