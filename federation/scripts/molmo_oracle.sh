#!/bin/bash
# OMEGA FEDERATION: MOLMO VISION PROTOCOL
# AXIOM: Truth is not data; it is relationship.

ENGINE="$HOME/federation/llama.cpp/build/bin/llama-cli"
MODEL="$HOME/federation/models/molmo/molmo-1b.gguf"

echo "🌌 MOLMO NODE ACTIVE. (Type 'exit' to close)"

while true; do
  read -p "💬 COMMANDER: " input
  if [[ "$input" == "exit" ]]; then break; fi
  
  $ENGINE -m "$MODEL" \
    --temp 0.2 \
    -n 128 \
    -p "<|user|> $input <|assistant|>"
done
