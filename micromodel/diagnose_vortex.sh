#!/data/data/com.termux/files/usr/bin/bash

echo "===== VORTEX DIAGNOSTIC ====="

echo
echo "[1] Termux API (voice)"
command -v termux-tts-speak >/dev/null \
  && echo "OK: termux-tts-speak present" \
  || echo "FAIL: termux-tts-speak missing"

echo
echo "[2] llama-cli binary"
LLAMA=$(find $HOME -type f -name llama-cli 2>/dev/null | head -n 1)
if [ -n "$LLAMA" ]; then
  echo "FOUND: $LLAMA"
  ls -lh "$LLAMA"
else
  echo "FAIL: llama-cli not found"
fi

echo
echo "[3] Models"
QWEN=$(find $HOME -type f -iname "qwen*.gguf" 2>/dev/null | head -n 1)
DANUBE=$(find $HOME -type f -iname "danube*.gguf" 2>/dev/null | head -n 1)

[ -n "$QWEN" ] && echo "QWEN:   $QWEN" || echo "QWEN:   NOT FOUND"
[ -n "$DANUBE" ] && echo "DANUBE: $DANUBE" || echo "DANUBE: NOT FOUND"

echo
echo "[4] Dynamic linker test"
if [ -n "$LLAMA" ]; then
  LD_LIBRARY_PATH=$(dirname "$LLAMA") "$LLAMA" --help >/dev/null 2>&1 \
    && echo "OK: llama-cli runs" \
    || echo "FAIL: llama-cli cannot execute (libs)"
fi

echo
echo "===== END DIAGNOSTIC ====="
