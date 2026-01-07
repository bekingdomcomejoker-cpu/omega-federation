#!/data/data/com.termux/files/usr/bin/bash
echo "Testing all models..."
cd ~/federation
for model in models/*.gguf; do
    echo "🔍 Testing $(basename "$model")"
    timeout 5s ./llama.cpp/main -m "$model" -p "test" -n 4 2>/dev/null && echo "  ✅ OK" || echo "  ❌ Failed"
done
