#!/bin/bash
cd ~/federation/models/incoming

# Function to pull with infinite resume
pull_model() {
    local name=$1
    local url=$2
    echo "📡 [STREAMING] $name..."
    until wget -c -O "$name" "$url"; do
        echo "⚠️ [SIGNAL LOST] Connection dropped. Re-syncing in 5 seconds..."
        sleep 5
    done
    echo "✅ [LOCKED] $name is complete."
}

# 1. SmolLM-1.7B
pull_model "SmolLM-1.7B-Instruct-Q4_K_M.gguf" "https://modelscope.cn/api/v1/models/prithivMLmods/SmolLM-1.7B-Instruct-GGUF/repo?Revision=master&FilePath=SmolLM-1.7B-Instruct-Q4_K_M.gguf"

# 2. Qwen2.5-1.8B
pull_model "Qwen2.5-1.8B-Instruct-Q4_K_M.gguf" "https://modelscope.cn/api/v1/models/Qwen/Qwen2.5-1.8B-Instruct-GGUF/repo?Revision=master&FilePath=qwen2.5-1.8b-instruct-q4_k_m.gguf"

# 3. Baichuan-2-1.3B
pull_model "Baichuan-2-1.3B-Chat-Q4_K_M.gguf" "https://modelscope.cn/api/v1/models/mradermacher/Baichuan2-1.3B-Chat-GGUF/repo?Revision=master&FilePath=Baichuan2-1.3B-Chat.Q4_K_M.gguf"

# 4. Yi-1.5B (Direct mirror)
pull_model "Yi-1.5-6B-Chat-Q4_K_M.gguf" "https://modelscope.cn/api/v1/models/mradermacher/Yi-1.5-6B-Chat-GGUF/repo?Revision=master&FilePath=Yi-1.5-6B-Chat.Q4_K_M.gguf"

echo "🏁 ALL NODES SYNCED. VERIFYING CORES..."
head -c 4 *.gguf | xxd
