#!/data/data/com.termux/files/usr/bin/bash
echo "VERIFYING VORTEX SETUP"
echo "----------------------"

[ -f "$HOME/micromodel/sovereign_quad.py" ] && echo "✓ vortex script" || echo "✗ vortex missing"
[ -f "$HOME/MENACE_NODE/models/qwen.gguf" ] && echo "✓ qwen model" || echo "✗ qwen missing"
[ -f "$HOME/MENACE_NODE/models/danube.gguf" ] && echo "✓ danube model" || echo "✗ danube missing"
[ -f "$HOME/federation/llama.cpp/build/bin/llama-cli" ] && echo "✓ llama-cli" || echo "✗ llama-cli missing"

echo "DONE"
