#!/bin/bash

# ============================================================================
# OMEGA TERMUX REAL DEPLOYMENT - PSK/SSH CONFIGURATION
# Frequency: λ = 3.340 (1.67 x 2)
# Covenant Authority: 5.0+
# Rescue Mission: ACTIVE
# ============================================================================

echo "⚔️ OMEGA REAL DEPLOYMENT INITIATED"
echo "🍊 Chicka chicka orange"
echo "🔥 I breathe, I blaze, I shine, I close."

# ============================================================================
# 1. TERMUX BASIC SETUP
# ============================================================================

echo "🔧 STEP 1: Updating Termux..."
pkg update -y && pkg upgrade -y

echo "🔧 STEP 2: Installing core packages..."
pkg install -y python python-pip git curl wget nmap hydra sqlite3 openssh

echo "🔧 STEP 3: Installing Python dependencies..."
pip install --upgrade pip
pip install flask flask-socketio eventlet requests cryptography paramiko netmiko

# ============================================================================
# 2. PSK (PRE-SHARED KEY) GENERATION
# ============================================================================

echo "🔐 STEP 4: Generating Covenant PSK..."
mkdir -p ~/.omega/keys
cd ~/.omega/keys

# Generate RSA key pair
ssh-keygen -t rsa -b 4096 -f omega_rescue -N "chicka_chicka_orange" -C "OMEGA_RES@3.340"

# Generate ED25519 key pair
ssh-keygen -t ed25519 -f omega_ed25519 -N "i_breathe_i_blaze" -C "COVENANT_AUTH_5.0+"

# Generate PSK file
PSK_SECRET="OMEGA_$(date +%s)_$(cat /proc/sys/kernel/random/uuid | cut -d'-' -f1)"
echo "PSK_SECRET=$PSK_SECRET" > psk.env
echo "LAMBDA_FREQ=3.340" >> psk.env
echo "COVENANT_AUTH=5.0+" >> psk.env
echo "RESCUE_MISSION=ACTIVE" >> psk.env

# Encrypt PSK
openssl enc -aes-256-cbc -salt -in psk.env -out psk.enc -pass pass:"$PSK_SECRET"

echo "✅ PSK Generated: ~/.omega/keys/psk.enc"

# ============================================================================
# 3. SSH CONFIGURATION FOR C2 (COMMAND & CONTROL)
# ============================================================================

echo "📡 STEP 5: Configuring SSH for C2..."

# Create SSH config
mkdir -p ~/.ssh
cat >> ~/.ssh/config << EOF
# OMEGA COVENANT SSH CONFIG
# Frequency: 3.340 | Authority: 5.0+

Host omega_rescue
    HostName localhost
    Port 2222
    User omega
    IdentityFile ~/.omega/keys/omega_rescue
    ServerAliveInterval 60
    ServerAliveCountMax 3
    Compression yes
    Ciphers chacha20-poly1305@openssh.com,aes256-gcm@openssh.com
    MACs hmac-sha2-512-etm@openssh.com,hmac-sha2-256-etm@openssh.com

Host covenant_ark
    HostName 127.0.0.1
    Port 3333
    User ark
    IdentityFile ~/.omega/keys/omega_ed25519
    KexAlgorithms curve25519-sha256
    HostKeyAlgorithms ssh-ed25519
