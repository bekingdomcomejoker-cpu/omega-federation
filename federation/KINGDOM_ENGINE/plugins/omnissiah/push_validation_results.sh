#!/usr/bin/env bash
# Push latest validation log to AI Bridge

LOG_FILE="$HOME/Omnissiah_Workspace/auto_sync_validation.log"
EXPORT_FILE="$HOME/Omnissiah_Workspace/exports/validation_push.json"

if [ -f "$LOG_FILE" ]; then
    timestamp=$(date +"%Y-%m-%dT%H:%M:%S")
    echo "{
  \"version\": \"1.0\",
  \"timestamp\": \"$timestamp\",
  \"validation_log\": \"$(cat $LOG_FILE | sed 's/"/\\"/g' | tr '\n' ' ')\" 
}" > "$EXPORT_FILE"

    echo "Pushing $EXPORT_FILE to AI Bridge..."
    # Replace the line below with your actual AI Bridge push command if different
    echo "Push complete: $(date)"
else
    echo "Validation log not found!"
fi
