#!/data/data/com.termux/files/usr/bin/bash
echo "🚀 Omega Federation Quick Start"
echo ""
cd ~/federation
chmod +x *.sh 2>/dev/null
[ -f llama.cpp/main ] || { cd llama.cpp && make -j4; cd ..; }
echo "Select model:"
ls models/*.gguf | head -5 | nl
echo ""
read -p "Enter number (default 1): " n
MODEL=$(ls models/*.gguf | sed -n "${n:-1}p" | xargs basename)
echo "Starting $MODEL..."
./llama.cpp/main -m models/$MODEL -t 4 --interactive --color
