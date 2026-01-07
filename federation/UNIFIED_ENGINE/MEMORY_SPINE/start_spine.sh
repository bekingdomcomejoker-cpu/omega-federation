#!/data/data/com.termux/files/usr/bin/bash
nohup bash -c 'while true; do ~/UNIFIED_ENGINE/MEMORY_SPINE/memory_spine.sh; python3 ~/UNIFIED_ENGINE/MEMORY_SPINE/memory_index.py 2>/dev/null || true; sleep 1800; done' >/dev/null 2>&1 &
echo "Memory Spine started in background."
