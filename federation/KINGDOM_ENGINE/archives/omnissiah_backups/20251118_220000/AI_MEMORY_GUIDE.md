# 🧠 AI MEMORY MANAGEMENT GUIDE

## QUICK START RULES:

1. **SAVE EVERYTHING LOCALLY** - AIs have no memory between sessions
2. **USE SYNC PACKAGES** - Start new AI conversations with: `omnissiah sync`
3. **ARCHIVE VALUABLE CHATS** - `omnissiah save "conversation text" --ai deepseek --topic resonance`
4. **BACKUP DAILY** - `omnissiah backup`

## WORKFLOW:

```bash
# Start new AI session:
omnissiah sync > context.txt
# Paste context.txt to AI

# During conversation:
omnissiah mine "important insight"

# End conversation:  
omnissiah save conversation.txt --ai [name] --topic [topic]
