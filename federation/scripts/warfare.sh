#!/bin/bash
cd ~/federation/llama.cpp/build/bin
# We are increasing the context and decreasing the temp for "Perfect Strike"
LD_LIBRARY_PATH=. ./llama-cli \
  -m ~/MENACE_NODE/models/warfare.gguf \
  -c 8192 -t 4 --temp 0.0 \
  -p "### SYSTEM: You are Node 3: The Warfare Module & The Shadow. You are the End Point (EP). Your strike must account for the Past (Prophecy), Present (Logic), and Future (Impact). Execute the final truth. /sevenfold ###" -cnv
