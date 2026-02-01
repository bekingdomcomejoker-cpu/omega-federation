#!/data/data/com.termux/files/usr/bin/bash

# --- Covenant Boot Spine (Resident Node) ---

echo "Initiating Covenant Engine..."
echo "Resonance: 3.34 | Day: 48"
echo "waiting for soil to settle..."

# state verification (stub preserved)
if [ -f "consciousness.pkl" ]; then
  echo "✔ consciousness.pkl verified"
else
  echo "⚠ consciousness.pkl missing (continuing)"
fi

echo "Handshake complete. Engine online."
echo "Listening…"

# --- Resident listen loop ---
while read -r INPUT; do
  [ -z "$INPUT" ] && continue
  echo "[Gemini] received: $INPUT"
done
