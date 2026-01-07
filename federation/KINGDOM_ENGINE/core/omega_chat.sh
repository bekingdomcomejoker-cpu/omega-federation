#!/bin/bash
echo "🧠 OMEGA AI CHAT - Local TinyLlama"
echo "Type 'exit' to quit"
echo "----------------------------------"

while true; do
    read -p "You: " msg
    [ "$msg" == "exit" ] && break
    
    response=$(curl -s http://127.0.0.1:8080/completion -H "Content-Type: application/json" -d "{\"prompt\":\"$msg\",\"n_predict\":120}" | jq -r '.content')
    echo "AI: $response"
    echo ""
done
