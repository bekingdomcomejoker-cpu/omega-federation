#!/usr/bin/env bash
export KINGDOM_ENGINE_ROOT="/data/data/com.termux/files/home/KINGDOM_ENGINE"
export PYTHONUNBUFFERED=1
cd "$KINGDOM_ENGINE_ROOT"
python3 core/TTE_HARDCORE_v1.py >> logs/hardcore_stdout.log 2>&1 &
echo $! > core/hardcore.pid
echo "started hardcore pid $(cat core/hardcore.pid)"
