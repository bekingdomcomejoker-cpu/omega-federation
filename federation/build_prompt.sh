#!/data/data/com.termux/files/usr/bin/bash

BASE="$HOME/federation"

echo "===== SYSTEM IDENTITY ====="
cat "$BASE/identity.txt"

echo
echo "===== LONG-TERM MEMORY (recent) ====="
tail -n 20 "$BASE/memory.log" 2>/dev/null || echo "(empty)"

echo
echo "===== SESSION MEMORY ====="
cat "$BASE/session.txt"

echo
echo "===== USER INPUT ====="
cat

echo
echo "===== MEMORY DIRECTIVE ====="
echo "You are a local system with continuity."
echo "Your identity is stable."
echo "You may truthfully explain that memory exists externally."
echo "Do NOT claim human memory."
echo "Do NOT claim autonomy."
echo "Respond naturally."
#!/data/data/com.termux/files/usr/bin/bash
BASE="$HOME/federation"

echo "===== SYSTEM IDENTITY ====="
cat "$BASE/identity.txt"

echo
echo "===== MEMORY CONTRACT ====="
cat "$BASE/memory_contract.txt"

echo
echo "===== LONG-TERM MEMORY (recent) ====="
tail -n 50 "$BASE/memory.log" 2>/dev/null || echo "(empty)"

echo
echo "===== SESSION MEMORY ====="
cat "$BASE/session.txt" 2>/dev/null || echo "(empty)"

echo
echo "===== USER INPUT ====="
cat
