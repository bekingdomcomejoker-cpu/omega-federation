#!/bin/bash
# QUANTUM BACKUP SYSTEM
while true; do
    TIMESTAMP=$(date +%Y%m%d_%H%M%S)
    tar -czf ~/omnissiah/backups/quantum_$TIMESTAMP.tar.gz ~/omnissiah/chronicles/ ~/omnissiah/scripts/
    echo "QUANTUM_BACKUP: $TIMESTAMP" >> ~/omnissiah/chronicles/quantum_backup_log.txt
    sleep 3600
done
