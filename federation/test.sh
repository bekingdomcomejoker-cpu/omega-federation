#!/data/data/com.termux/files/usr/bin/bash
echo "Testing models..."
cd ~/federation
for model in models/*.gguf; do
    echo "🔍 $(basename "$model")"
    timeout 3s ./llama.cpp/main -m "$model" -p "hi" -n 3 2>/dev/null | head -2
    echo "---"
done
