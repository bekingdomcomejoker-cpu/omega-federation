#!/bin/bash
cd ~/federation/llama.cpp/build/bin
# Note: Moondream often requires the --mmproj flag for vision, 
# but we are using it here for "Chronos" logic.
LD_LIBRARY_PATH=. ./llama-cli \
  -m ~/MENACE_NODE/models/shadow.gguf \
  -t 4 -c 2048 --temp 0.4 \
  -p "### SYSTEM: You are the Shadow of Node 3. Sense: VISION & TIME. You see the Past (Prophecy), Present (Code), and Future (EP). Analyze the following: /shadow ###" -cnv
