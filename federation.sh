#!/bin/bash

INPUT="$*"
DECISION=$(~/sentinel.sh "$INPUT")

if [ "$DECISION" = "ESCALATE" ]; then
  echo "[ESCALATED — external review required]"
else
  ~/wire.sh "$INPUT"
fi
