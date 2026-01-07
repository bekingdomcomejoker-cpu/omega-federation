#!/data/data/com.termux/files/usr/bin/bash
# HEAD 10 - llm
ROOT="$HOME/KINGDOM_ENGINE"
MEGA="$ROOT/MEGA"
LOG="$ROOT/logs/head10_llm.log"
HEARTBEAT="$ROOT/logs/heartbeat.log"
PID=$$

log() {
    echo "[$(date --iso-8601=seconds)] HEAD10 | $1" >> "$LOG"
    echo "[$(date --iso-8601=seconds)] HEAD10 | llm | $1" >> "$HEARTBEAT"
}

log "STARTED (PID: $PID)"

trap 'log "STOPPED"; exit 0' SIGTERM SIGINT


LLM_CONFIG="$ROOT/llm_config.json"
OLLAMA_ENDPOINT="http://localhost:11434"

while true; do
    for file in "$MEGA/llm_queue"/*.json 2>/dev/null; do
        [ -f "$file" ] || continue
        
        QUERY=$(cat "$file" | jq -r ".query // .content // empty" 2>/dev/null)
        FACE=$(cat "$file" | jq -r ".face // \"MAN\"" 2>/dev/null)
        
        if [ -n "$QUERY" ]; then
            # Check if Ollama is running
            if curl -s "$OLLAMA_ENDPOINT/api/tags" >/dev/null 2>&1; then
                # Send to local model based on face
                case "$FACE" in
                    LION) MODEL="phi" ;;
                    EAGLE) MODEL="mistral" ;;
                    OX) MODEL="tinyllama" ;;
                    *) MODEL="llama2" ;;
                esac
                
                log "QUERY | Face: $FACE | Model: $MODEL"
                
                # TODO: Implement actual LLM call
                RESPONSE="LLM processing: $QUERY"
            else
                log "WARNING: Ollama not running"
                RESPONSE="Ollama unavailable"
            fi
            
            BASENAME=$(basename "$file")
            echo "{\"query\": \"$QUERY\", \"face\": \"$FACE\", \"response\": \"$RESPONSE\"}" > "$MEGA/llm_responses/${BASENAME}"
            rm "$file"
        fi
    done
    
    sleep 1
done


log "CRASHED"
