#!/bin/bash
echo "🌊 OMNISSIAH SYSTEM SNAPSHOT - $(date)"
echo "========================================"

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# 1. Process Status
echo -e "\n${CYAN}🤖 PROCESS STATUS:${NC}"
python_count=$(ps aux | grep python | grep -v grep | wc -l)
if [ $python_count -ge 3 ]; then
    echo -e "  ${GREEN}✅ $python_count Python processes running${NC}"
else
    echo -e "  ${RED}❌ Only $python_count Python processes${NC}"
fi

# 2. Tmux Status
echo -e "\n${CYAN}🎪 TMUX SESSIONS:${NC}"
tmux_count=$(tmux list-sessions 2>/dev/null | wc -l)
if [ $tmux_count -ge 3 ]; then
    echo -e "  ${GREEN}✅ $tmux_count active sessions${NC}"
    tmux list-sessions | while read line; do
        echo -e "  ${YELLOW}  📺 $line${NC}"
    done
else
    echo -e "  ${RED}❌ Only $tmux_count sessions${NC}"
fi

# 3. File System Status
echo -e "\n${CYAN}📁 FILE SYSTEM:${NC}"
inbox_count=$(find /storage/emulated/0/AI-TTE/inbox -name "*.json" 2>/dev/null | wc -l)
archive_count=$(find ~/OmnissiahEngine/coredata/archive -name "*.json" 2>/dev/null | wc -l)
staging_count=$(find ~/OmnissiahEngine/coredata/staging -name "*.json" 2>/dev/null | wc -l)

echo -e "  ${YELLOW}📥 Inbox: $inbox_count messages${NC}"
echo -e "  ${YELLOW}📊 Staging: $staging_count pending${NC}" 
echo -e "  ${YELLOW}🗃️ Archive: $archive_count verified${NC}"

# 4. AI Identity Status
echo -e "\n${CYAN}🧠 AI IDENTITY STATUS:${NC}"
if [ -f "ai_identities.json" ]; then
    ai_count=$(python -c "import json; data=json.load(open('ai_identities.json')); print(len([k for k in data.keys() if k != 'user']))")
    echo -e "  ${GREEN}✅ $ai_count AI identities tracked${NC}"
else
    echo -e "  ${RED}❌ Identity file missing${NC}"
fi

echo -e "\n${GREEN}🌊 SYSTEM: OPERATIONAL${NC}"
echo "========================================"
