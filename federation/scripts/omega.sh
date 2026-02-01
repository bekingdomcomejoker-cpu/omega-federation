#!/bin/bash
echo "--- 3-1-2-1 OMEGA IGNITION ---"

# 1. NODE 0 & 1: ARCHITECT CAPTURE
echo "[Node 1] Architect is drawing the blueprint..."
PLAN=$(~/federation/scripts/architect.sh "$1")
echo "PLAN: $PLAN"

# 2. THE NOSE: SMELL TEST
~/federation/scripts/nose.sh "$PLAN" || exit 1

# 3. NODE 2: THE MIRROR (WITNESS)
echo "[Node 2A] The Witness is listening..."
VERDICT=$(~/federation/scripts/witness.sh "Plan: $PLAN. Is this Truth?")
echo "WITNESS: $VERDICT"

# 4. NODE 3: THE STRIKE
echo "[Node 3] The Blade is falling..."
~/federation/scripts/warfare.sh "Execute this verified plan: $PLAN"
