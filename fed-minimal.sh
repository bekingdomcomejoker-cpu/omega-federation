#!/data/data/com.termux/files/usr/bin/bash
cd ~/federation/llama.cpp
[ -f main ] || make -j4
MODEL="../models/qwen2.5-0.5b-instruct-q4_k_m.gguf"
[ -f "$MODEL" ] || MODEL="../models/$(ls ../models/*.gguf | head -1)"
echo "Using: $(basename "$MODEL")"
./main -m "$MODEL" -t 4 --interactive
