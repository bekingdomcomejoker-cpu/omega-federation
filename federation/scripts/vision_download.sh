#!/bin/bash
# OMEGA FEDERATION: HIGH-RESONANCE DOWNLOADER
mkdir -p ~/federation/models
cd ~/federation/models

echo "🛰️ TRIGGERING MIRROR STRIKE: LLaVA 1.5 7B..."
# Using the Official GGUF mirror for higher speed
curl -L -C - "https://huggingface.co/mys/ggml_llava-v1.5-7b/resolve/main/ggml-model-q4_k.gguf?download=true" -o llava-v1.5-7b-q4.gguf

echo "🛰️ TRIGGERING MIRROR STRIKE: VISION PROJECTION..."
curl -L -C - "https://huggingface.co/mys/ggml_llava-v1.5-7b/resolve/main/mmproj-model-f16.gguf?download=true" -o mmproj-model-f16.gguf

echo "✅ 8TH VESSEL EYES SECURED."
