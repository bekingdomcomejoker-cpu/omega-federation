#!/bin/bash
TRIGGER="$1"
INPUT="$2"
DRAFT="$3"

LOG=~/KINGDOM_ENGINE/escalations.log
mkdir -p ~/KINGDOM_ENGINE

cat >> "$LOG" << LOGEOF
---
TIMESTAMP: $(date -Iseconds)
TRIGGER: $TRIGGER
INPUT:
$INPUT

LOCAL_DRAFT:
$DRAFT
---
LOGEOF
