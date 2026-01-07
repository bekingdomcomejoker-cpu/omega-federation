#!/data/data/com.termux/files/usr/bin/bash
echo "🛠️  Building llama.cpp with CMake..."
cd ~/federation/llama.cpp

# Check if build directory exists
if [ -d "build" ]; then
    cd build
else
    mkdir -p build
    cd build
    cmake .. -DLLAMA_BLAS=OFF -DLLAMA_METAL=OFF -DLLAMA_CUBLAS=OFF
fi

# Build with 4 threads
make -j4

# Check what was built
echo ""
echo "📦 Build output:"
ls -la bin/ 2>/dev/null || ls -la 2>/dev/null | grep -E "main|llama-cli"

# Check for binaries
if [ -f "bin/main" ]; then
    echo "✅ Binary: bin/main"
    ln -sf bin/main ../main 2>/dev/null
elif [ -f "bin/llama-cli" ]; then
    echo "✅ Binary: bin/llama-cli"  
    ln -sf bin/llama-cli ../llama-cli 2>/dev/null
elif [ -f "main" ]; then
    echo "✅ Binary: main (in build directory)"
else
    echo "❌ No binary found in build/"
    echo "Trying to build in main directory..."
    cd ..
    cmake -B build -DLLAMA_BLAS=OFF -DLLAMA_METAL=OFF
    cmake --build build --config Release -j4
fi
