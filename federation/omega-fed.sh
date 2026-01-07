#!/data/data/com.termux/files/usr/bin/bash
FED_HOME="$HOME/federation"
MODEL_DIR="$FED_HOME/models"

# Use llama-cli from KINGDOM_ENGINE build
LLAMA="$FED_HOME/KINGDOM_ENGINE/models/llama_cpp/build/bin/llama-cli"

echo "✅ Using: $LLAMA"

clear
echo "╔══════════════════════════════════════════╗"
echo "║     OMEGA FEDERATION - ACTIVE MODELS    ║"
echo "║      (Using llama-cli)                  ║"
echo "╚══════════════════════════════════════════╝"

# Filter out small/broken models (< 10MB)
echo ""
echo "📦 VALID MODELS (>10MB):"
valid_models=()
i=0
for model in "$MODEL_DIR"/*.gguf; do
    if [ -f "$model" ]; then
        size=$(stat -c%s "$model" 2>/dev/null || echo "0")
        if [ $size -gt 10000000 ]; then  # > 10MB
            valid_models+=("$model")
            i=$((i+1))
            size_mb=$((size/1024/1024))
            echo "  $i. $(basename "$model") (${size_mb}MB)"
        fi
    fi
done

if [ ${#valid_models[@]} -eq 0 ]; then
    echo "❌ No valid models found"
    exit 1
fi

echo ""
read -p "🚀 SELECT MODEL (1-$i): " choice

if ! [[ "$choice" =~ ^[0-9]+$ ]] || [ "$choice" -lt 1 ] || [ "$choice" -gt $i ]; then
    echo "❌ Invalid choice"
    exit 1
fi

MODEL="${valid_models[$((choice-1))]}"
echo ""
echo "🚀 Launching $(basename "$MODEL")..."
echo "Type '//exit' to quit"
echo ""

# Run llama-cli
"$LLAMA" -m "$MODEL" \
    -t 4 \
    -c 2048 \
    --color \
    --interactive \
    --reverse-prompt "User:" \
    --in-prefix " " \
    --in-suffix " "
