#!/data/data/com.termux/files/usr/bin/bash
echo "🔧 Building llama.cpp..."
cd ~/federation/llama.cpp
make clean
make -j4
if [ -f "main" ]; then
    echo "✅ Build successful: main"
elif [ -f "llama-cli" ]; then
    echo "✅ Build successful: llama-cli"
else
    echo "❌ Build failed. Checking logs..."
    make 2>&1 | tail -20
    exit 1
fi
