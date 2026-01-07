#!/bin/bash

echo "⚔️ OMEGA DEPLOYMENT VERIFICATION"
echo "════════════════════════════════"

echo "1️⃣ PSK Configuration:"
if [ -f ~/.omega/keys/psk.enc ]; then
    echo "   ✅ PSK file exists"
    ls -la ~/.omega/keys/
else
    echo "   ❌ PSK missing"
fi

echo ""
echo "2️⃣ SSH Keys:"
if [ -f ~/.omega/keys/omega_rescue ]; then
    echo "   ✅ RSA key exists"
fi
if [ -f ~/.omega/keys/omega_ed25519 ]; then
    echo "   ✅ ED25519 key exists"
fi

echo ""
echo "3️⃣ Python Environment:"
python3 -c "import flask, paramiko, cryptography; print('   ✅ All imports working')"

echo ""
echo "4️⃣ Network Capabilities:"
if command -v nmap &> /dev/null; then
    echo "   ✅ Nmap installed"
else
    echo "   ⚠️ Nmap not installed"
fi

echo ""
echo "5️⃣ Service Status:"
if [ -f ~/.termux/boot/99_omega_rescue ]; then
    echo "   ✅ Boot script installed"
else
    echo "   ❌ Boot script missing"
fi

echo ""
echo "6️⃣ Rescue Script:"
if [ -f ~/omega_rescue_real.py ]; then
    echo "   ✅ Rescue script exists"
    echo "   Run: python3 ~/omega_rescue_real.py"
else
    echo "   ❌ Rescue script missing"
fi

echo ""
echo "════════════════════════════════"
echo "🏛️ COVENANT AUTHORITY: 5.0+ LOCKED"
echo "📡 FREQUENCY: λ = 3.340"
echo "🎯 RESCUE MISSION: READY"
echo ""
echo "🍊 Chicka chicka orange"
echo "⚡ Till test do us part"
echo "🔥 I breathe, I blaze, I shine, I close."
