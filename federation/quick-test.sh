#!/data/data/com.termux/files/usr/bin/bash
echo "Quick test..."
cd ~/federation/llama.cpp

# Build if needed
if [ ! -f "build/bin/main" ] && [ ! -f "build/bin/llama-cli" ]; then
    echo "Building..."
    mkdir -p build
    cd build
    cmake .. -DLLAMA_BLAS=OFF
    make -j4
    cd ..
fi

# Find binary
if [ -f "build/bin/main" ]; then
    BIN="build/bin/main"
elif [ -f "build/bin/llama-cli" ]; then
    BIN="build/bin/llama-cli"
elif [ -f "build/main" ]; then
    BIN="build/main"
else
    echo "No binary found"
    exit 1
fi

# Test with smallest model
MODEL="../models/qwen2.5-0.5b-instruct-q4_k_m.gguf"
if [ -f "$MODEL" ]; then
    echo "Testing $MODEL..."
    "$BIN" -m "$MODEL" -p "Hello" -n 20 -t 2
else
    # Get first model
    FIRST_MODEL=$(ls ../models/*.gguf 2>/dev/null | head -1)
    echo "Testing $FIRST_MODEL..."
    "$BIN" -m "$FIRST_MODEL" -p "Test" -n 10 -t 2
fi
