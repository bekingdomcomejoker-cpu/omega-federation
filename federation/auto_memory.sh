#!/data/data/com.termux/files/usr/bin/bash
# Automatic minimal memory persistence layer
# Append-only, bounded, human-readable

BASE="$HOME/federation"
MEM="$BASE/memory.log"
SESSION="$BASE/session.txt"

MAX_LINES=200   # hard cap for memory size

input="$1"
output="$2"

# Heuristic: only store high-signal lines
if echo "$input $output" | grep -qiE \
"(prefer|important|remember|identity|purpose|name|always|never|core|principle)"; then
  echo "$(date -Is) | USER: $input" >> "$MEM"
  echo "$(date -Is) | MODEL: $output" >> "$MEM"
fi

# Enforce bounded memory
tail -n "$MAX_LINES" "$MEM" > "$MEM.tmp" && mv "$MEM.tmp" "$MEM"

# Always append to session log
echo "USER: $input" >> "$SESSION"
echo "MODEL: $output" >> "$SESSION"
#!/data/data/com.termux/files/usr/bin/bash
BASE="$HOME/federation"
TS=$(date -Is)

echo "$TS | USER: $1" >> "$BASE/memory.log"
echo "$TS | MODEL: $2" >> "$BASE/memory.log"

echo "USER: $1" >> "$BASE/session.txt"
echo "MODEL: $2" >> "$BASE/session.txt"
#!/data/data/com.termux/files/usr/bin/bash

BASE="$HOME/federation"
TS=$(date -Is)

echo "$TS | USER: $1" >> "$BASE/memory.log"
echo "$TS | MODEL: $2" >> "$BASE/memory.log"
