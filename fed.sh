#!/data/data/com.termux/files/usr/bin/bash
cd ~/federation
if [ ! -f llama.cpp/main ]; then
    echo "Building llama.cpp..."
    cd llama.cpp && make -j4 && cd ..
fi
MODEL="${1:-Phi-3.5-mini-instruct-Q4_K_M.gguf}"
echo "🚀 Launching $MODEL"
./llama.cpp/main -m models/$MODEL -t 4 --interactive --color
