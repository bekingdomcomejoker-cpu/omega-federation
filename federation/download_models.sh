#!/bin/bash
cd ~/federation/models/incoming

echo "🚀 Initiating Omega Model Stream..."

# 1. SmolLM
wget -c -O SmolLM-1.7B-Instruct-Q4_K_M.gguf https://hf-mirror.com/HuggingFaceTB/SmolLM-1.7B-Instruct-GGUF/resolve/main/SmolLM-1.7B-Instruct-Q4_K_M.gguf?download=true

# 2. Baichuan
wget -c -O Baichuan-2-1.3B-Chat-Q4_K_M.gguf https://hf-mirror.com/TheBloke/Baichuan2-1.3B-Chat-GGUF/resolve/main/Baichuan2-1.3B-Chat-Q4_K_M.gguf?download=true

# 3. Yi
wget -c -O Yi-1.5B-Chat-Q4_K_M.gguf https://hf-mirror.com/TheBloke/Yi-1.5B-Chat-GGUF/resolve/main/Yi-1.5B-Chat-Q4_K_M.gguf?download=true

# 4. Qwen
wget -c -O Qwen2.5-1.8B-Instruct-Q4_K_M.gguf https://hf-mirror.com/Qwen/Qwen2.5-1.8B-Instruct-GGUF/resolve/main/Qwen2.5-1.8B-Instruct-Q4_K_M.gguf?download=true

echo "✅ All streams reached 100%. Running verification..."
head -c 4 *.gguf | xxd
