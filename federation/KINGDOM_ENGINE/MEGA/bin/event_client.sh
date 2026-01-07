#!/data/data/com.termux/files/usr/bin/bash

MSG="$1"
BUS="$HOME/KINGDOM_ENGINE/MEGA/bus/inbox"

mkdir -p "$BUS"

ts() { date -Iseconds; }

json="{\"ts\":\"$(ts)\",\"type\":\"generic\",\"payload\":\"$MSG\"}"

id=$(date +%s%N)
echo "$json" > "$BUS/$id.json"
