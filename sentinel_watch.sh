#!/bin/bash
# SENTINEL: DRIVE INTEGRITY PULSE
while true; do
  find ~/KINGDOM_ENGINE -type f -exec sha256sum {} + > ~/drive_manifest.sig
  sleep 60
done
