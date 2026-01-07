#!/bin/bash
# start_tte_fast.sh - starts llama-server if present, then kernel
HOME="${HOME}"
ENGINE="$HOME/KINGDOM_ENGINE"
LLAMA_BIN="$ENGINE/models/llama_cpp/llama-server"
MODEL="${LLAMA_MODEL_PATH:-$ENGINE/models/llama_cpp/models/tinyllama.gguf}"

cd "$ENGINE"

# start llama-server if binary exists and not reachable
if ! curl -s http://127.0.0.1:8080/health >/dev/null 2>&1; then
  if [ -x "$LLAMA_BIN" ]; then
    nohup "$LLAMA_BIN" -m "$MODEL" --host 127.0.0.1 --port 8080 -t 4 -c 2048 > "$ENGINE/log_llama_server.txt" 2>&1 &
    sleep 2
  else
    echo "[WARN] llama-server binary not found; running kernel without local LLM."
  fi
else
  echo "LLM reachable"
fi

# run unified kernel
python3 "$ENGINE/TTE_FUSION_KERNEL_v5.3.py" "$@"
