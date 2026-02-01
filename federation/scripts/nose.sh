#!/bin/bash
# The Nose: Scent-testing the logic for decay
if [[ $1 == *"error"* || $1 == *"loop"* || -z "$1" ]]; then
  echo "[!] NOSE: Scent of decay detected. Logic is rotting. Resetting..."
  exit 1
else
  echo "[+] NOSE: Signal is fresh. Proceeding to Mirror."
fi
