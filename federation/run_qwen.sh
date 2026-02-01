#!/data/data/com.termux/files/usr/bin/bash

MODEL="$HOME/federation/models/qwen2.5-0.5b-instruct-q4_k_m.gguf"
BASE="$HOME/federation"

read -p "> " USER_INPUT

PROMPT="$(echo "$USER_INPUT" | "$BASE/build_prompt.sh")"

RESPONSE=$(llama-cli \
  -m "$MODEL" \
  -t 4 \
  -c 1024 \
  -n 256 \
  --temp 0.7 \
  --top-k 40 \
  --top-p 0.9 \
  --repeat-penalty 1.1 \
  --batch-size 64 \
  --prompt "$PROMPT"
)

echo "$RESPONSE"

"$BASE/auto_memory.sh" "$USER_INPUT" "$RESPONSE"
#!/data/data/com.termux/files/usr/bin/bash

MODEL="$HOME/federation/models/qwen2.5-0.5b-instruct-q4_k_m.gguf"
PROMPT_BUILDER="$HOME/federation/build_prompt_v2.sh"

while true; do
  read -r -p "> " USER_INPUT || exit 0

  PROMPT=$(echo "$USER_INPUT" | $PROMPT_BUILDER)

  RESPONSE=$(llama-cli \
    -m "$MODEL" \
    -t 4 \
    -c 1536 \
    -n 256 \
    --temp 0.6 \
    --top-k 40 \
    --top-p 0.9 \
    --repeat-penalty 1.1 \
    --batch-size 128 \
    --prompt "$PROMPT"
  )

  echo "$RESPONSE"

  $HOME/federation/auto_memory.sh "$USER_INPUT" "$RESPONSE"
  echo "USER: $USER_INPUT" >> $HOME/federation/session.txt
  echo "MODEL: $RESPONSE" >> $HOME/federation/session.txt
done
