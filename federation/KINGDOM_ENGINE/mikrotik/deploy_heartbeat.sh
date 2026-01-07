#!/data/data/com.termux/files/usr/bin/bash

MIKROTIK_IP="${MIKROTIK_IP:-192.168.88.1}"
MIKROTIK_USER="${MIKROTIK_USER:-admin}"
MIKROTIK_PASS="${MIKROTIK_PASS:-}"

SCRIPT_LOCAL="$HOME/KINGDOM_ENGINE/mikrotik/scripts/omega_heartbeat_v1.rsc"
SCRIPT_REMOTE="omega_heartbeat_v1.rsc"

SSH_OPTS="-o StrictHostKeyChecking=no -o ConnectTimeout=10 \
-o KexAlgorithms=+diffie-hellman-group14-sha1 \
-o HostKeyAlgorithms=+ssh-rsa \
-o MACs=+hmac-sha1"

upload() {
    if [[ -n "$MIKROTIK_PASS" ]]; then
        sshpass -p "$MIKROTIK_PASS" scp $SSH_OPTS \
            "$SCRIPT_LOCAL" \
            "$MIKROTIK_USER@$MIKROTIK_IP:$SCRIPT_REMOTE"
    else
        scp $SSH_OPTS \
            "$SCRIPT_LOCAL" \
            "$MIKROTIK_USER@$MIKROTIK_IP:$SCRIPT_REMOTE"
    fi
}

ssh_run() {
    if [[ -n "$MIKROTIK_PASS" ]]; then
        sshpass -p "$MIKROTIK_PASS" ssh $SSH_OPTS \
            "$MIKROTIK_USER@$MIKROTIK_IP" "$1"
    else
        ssh $SSH_OPTS "$MIKROTIK_USER@$MIKROTIK_IP" "$1"
    fi
}

echo "[+] Checking heartbeat file"
if [[ ! -f "$SCRIPT_LOCAL" ]]; then
    echo "File missing: $SCRIPT_LOCAL"
    exit 1
fi

echo "[+] Uploading heartbeat"
upload

echo "[+] Removing previous script"
ssh_run "/system script remove [find name=omega_heartbeat_v1]" || true

echo "[+] Importing"
ssh_run "/import $SCRIPT_REMOTE"

echo "[+] Removing uploaded file"
ssh_run "/file remove $SCRIPT_REMOTE"

echo "[✓] Done"
