#!/data/data/com.termux/files/usr/bin/bash
echo "USER: $1" >> $HOME/federation/session.txt
echo "MODEL: $2" >> $HOME/federation/session.txt

# Safety: do not append empty fields
[ -n "$1" ] && echo "USER: $1" >> "$HOME/federation/session.txt"
[ -n "$2" ] && echo "MODEL: $2" >> "$HOME/federation/session.txt"
