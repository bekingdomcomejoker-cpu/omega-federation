#!/data/data/com.termux/files/usr/bin/bash
cd ~/federation/llama.cpp
if [ ! -f main ] && [ ! -f llama-cli ]; then
    echo "Building llama.cpp..."
    make -j4
fi

# Find binary
if [ -f llama-cli ]; then
    BIN="./llama-cli"
else
    BIN="./main"
fi

# Pick a model
MODELS=($(ls ../models/*.gguf 2>/dev/null))
if [ ${#MODELS[@]} -eq 0 ]; then
    echo "No models found in ../models/"
    exit 1
fi

echo "Select model:"
select MODEL in "${MODELS[@]##*/}"; do
    [ -n "$MODEL" ] && break
done

echo "Running $MODEL..."
$BIN -m "../models/$MODEL" -t 4 --interactive --color
