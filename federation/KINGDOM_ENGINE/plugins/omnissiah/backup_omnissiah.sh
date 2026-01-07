#!/bin/bash
# OMNISSIAH BACKUP SCRIPT (Internal Storage Version)

DATE=$(date +%Y%m%d_%H%M%S)
WORKSPACE="$HOME/Omnissiah_Workspace"
BACKUP_DIR="$HOME/Omnissiah_Backups/$DATE"

echo "💾 Creating backup: $DATE"
mkdir -p "$BACKUP_DIR"

# Copy all system files
cp "$WORKSPACE"/*.py "$BACKUP_DIR/" 2>/dev/null || true
cp "$WORKSPACE"/*.json "$BACKUP_DIR/" 2>/dev/null || true
cp "$WORKSPACE"/*.jsonl "$BACKUP_DIR/" 2>/dev/null || true
cp "$WORKSPACE"/*.txt "$BACKUP_DIR/" 2>/dev/null || true
cp "$WORKSPACE"/*.md "$BACKUP_DIR/" 2>/dev/null || true

# Copy conversation archives
if [ -d "$WORKSPACE/conversations" ]; then
    cp -r "$WORKSPACE/conversations" "$BACKUP_DIR/"
fi

# Copy additional folders if they exist
for folder in archives backups conversation_archive exports logs resonance_archive screenshot_archive; do
    if [ -d "$WORKSPACE/$folder" ]; then
        cp -r "$WORKSPACE/$folder" "$BACKUP_DIR/"
    fi
done

# Create backup manifest
cat > "$BACKUP_DIR/manifest.txt" << MANIFEST
OMNISSIAH BACKUP
Date: $DATE
Files: $(ls -1 "$BACKUP_DIR" | wc -l)
Size: $(du -sh "$BACKUP_DIR" | cut -f1)
MANIFEST

echo "✅ Backup complete: $BACKUP_DIR"
echo "   Files: $(ls -1 "$BACKUP_DIR" | wc -l)"
echo "   Size: $(du -sh "$BACKUP_DIR" | cut -f1)"
