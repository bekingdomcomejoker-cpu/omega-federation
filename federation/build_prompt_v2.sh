#!/data/data/com.termux/files/usr/bin/bash

BASE="$HOME/federation"

echo "===== SYSTEM IDENTITY ====="
sed -n '1,40p' "$BASE/identity.txt"

echo
echo "===== LONG-TERM MEMORY (summary) ====="
tail -n 10 "$BASE/memory.log" 2>/dev/null || echo "(empty)"

echo
echo "===== SESSION MEMORY (recent) ====="
tail -n 10 "$BASE/session.txt" 2>/dev/null || echo "(empty)"

echo
echo "===== USER INPUT ====="
cat
