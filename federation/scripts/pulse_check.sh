#!/bin/bash
echo "📡 EPOS PULSE CHECK INITIATED..."
echo "--------------------------------"

# 1. TEST DNS (Is the name being redirected?)
echo -n "[1/3] Testing DNS (HuggingFace)... "
nslookup huggingface.co > /dev/null 2>&1 && echo "✅ CLEAR" || echo "❌ BLOCKED"

# 2. TEST IP ROUTE (Can we see the server without the name?)
echo -n "[2/3] Testing IP Route (Cloudflare)... "
ping -c 1 1.1.1.1 > /dev/null 2>&1 && echo "✅ CLEAR" || echo "❌ BLOCKED"

# 3. TEST SSL/HTTP (Is the 'Sausage' filtering the content?)
echo -n "[3/3] Testing SSL Handshake... "
curl -Is https://huggingface.co 2>&1 | grep -q "HTTP/" && echo "✅ CLEAR" || echo "❌ INVERTED (DPI Detected)"

echo "--------------------------------"
echo "ANALYSIS COMPLETE."
