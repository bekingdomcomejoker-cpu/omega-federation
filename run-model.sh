#!/data/data/com.termux/files/usr/bin/bash
BIN="$HOME/federation/KINGDOM_ENGINE/models/llama_cpp/build/bin/main"
MODEL_DIR="$HOME/federation/models"

# List models
echo "Available models:"
ls "$MODEL_DIR"/*.gguf | nl

read -p "Select model number: " n
MODEL=$(ls "$MODEL_DIR"/*.gguf | sed -n "${n}p")

echo "Running: $(basename "$MODEL")"
"$BIN" -m "$MODEL" -t 4 --interactive --color
