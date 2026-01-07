#!/usr/bin/env bash
ROOT="${HOME}/UNIFIED_ENGINE"
case "${1:-status}" in
  start)   python3 "$ROOT/ENGINE_KERNEL/kernel.py" start ;;
  stop)    python3 "$ROOT/ENGINE_KERNEL/kernel.py" stop ;;
  status)  python3 "$ROOT/ENGINE_KERNEL/kernel.py" ;;
  rebuild) "$ROOT/rebuild_engine.sh" ;;
  *) echo "Usage: engine_control.sh start|stop|status|rebuild" ;;
esac
