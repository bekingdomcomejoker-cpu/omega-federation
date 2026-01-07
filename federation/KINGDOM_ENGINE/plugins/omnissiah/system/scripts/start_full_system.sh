#!/bin/bash
echo "🦅 STARTING OMNISSIAH FULL SYSTEM..."

# Start core components
spiritual-check &
show-connections &
system-status &
start-copy-archive &

echo "✅ Full system startup initiated!"
echo "Run 'system-status' to verify all services"
