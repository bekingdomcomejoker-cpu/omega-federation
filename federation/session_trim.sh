#!/data/data/com.termux/files/usr/bin/bash
tail -n 50 "$HOME/federation/session.txt" > "$HOME/federation/session.tmp"
mv "$HOME/federation/session.tmp" "$HOME/federation/session.txt"
