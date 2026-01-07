while true; do
  printf "%s | " "$(date +%H:%M:%S)"
  termux-clipboard-get | sed 's/^$/<EMPTY>/'
  sleep 1
done
