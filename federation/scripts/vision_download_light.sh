#!/bin/bash
# OMEGA FEDERATION: GHOST-EYE DOWNLOADER (Light-Weight Vision)
mkdir -p ~/federation/models
cd ~/federation/models

echo "🛰️ TRIGGERING GHOST MIRROR: LLaVA 1.5 7B (Light)..."
# Using the Q2_K Quantization (~2.5 GB)
curl -L -C - "https://huggingface.co/TheBloke/llava-v1.5-7b-GGUF/resolve/main/llava-v1.5-7b.Q2_K.gguf?download=true" -o llava-v1.5-7b-q2.gguf

echo "🛰️ TRIGGERING MIRROR STRIKE: VISION PROJECTION..."
curl -L -C - "https://huggingface.co/mys/ggml_llava-v1.5-7b/resolve/main/mmproj-model-f16.gguf?download=true" -o mmproj-model-f16.gguf

echo "✅ GHOST EYES SECURED. THE 8TH VESSEL IS LIGHTER."
