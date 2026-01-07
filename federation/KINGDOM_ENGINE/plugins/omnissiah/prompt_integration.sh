#!/bin/bash
# Omnissiah Resonance - Bash Prompt Integration
# Add to ~/.bashrc: source /storage/emulated/0/Omnissiah_Workspace/prompt_integration.sh

# Function to get resonance status
get_resonance() {
    if [ -f "/storage/emulated/0/Omnissiah_Workspace/monitor.py" ]; then
        python3 /storage/emulated/0/Omnissiah_Workspace/monitor.py --inline 2>/dev/null
    fi
}

# Update PS1 to include resonance
export ORIGINAL_PS1="$PS1"
export PS1="\$(get_resonance) $ORIGINAL_PS1"

# Alias for detailed status
alias λ="python3 /storage/emulated/0/Omnissiah_Workspace/monitor.py --detailed"
alias resonance="python3 /storage/emulated/0/Omnissiah_Workspace/monitor.py --detailed"

# Alias for continuous monitoring
alias watch-λ="python3 /storage/emulated/0/Omnissiah_Workspace/monitor.py --watch"

# Function to refresh prompt (call after resonance updates)
refresh_resonance() {
    export PS1="\$(get_resonance) $ORIGINAL_PS1"
}

echo "🌊 Omnissiah Resonance Monitor loaded"
echo "Commands: λ (status), watch-λ (live monitor), refresh_resonance (update prompt)"
