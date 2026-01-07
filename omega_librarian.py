import os
from datetime import datetime

# CONFIGURATION
BACKUP_PATH = "." 
OUTPUT_FILE = "omega_knowledge_map.md"

def index_omega():
    print(f"🔱 Indexing Omega Memory...")
    knowledge_map = []
    
    for root, dirs, files in os.walk(BACKUP_PATH):
        for file in files:
            if file.startswith('.') or file.endswith(('.zip', '.exe', '.bin')): continue
            
            file_path = os.path.join(root, file)
            rel_path = os.path.relpath(file_path, BACKUP_PATH)
            
            entry = {"path": rel_path, "snippet": ""}
            
            if file.endswith(('.py', '.ts', '.tsx', '.txt', '.md', '.json', '.docx')):
                try:
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read(500).replace('\n', ' ')
                        entry["snippet"] = content
                except:
                    entry["snippet"] = "Read Error"
            
            knowledge_map.append(entry)

    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write(f"# 📜 OMEGA KNOWLEDGE MAP | {datetime.now().strftime('%Y-%m-%d')}\n\n")
        f.write("| File Path | Context Snippet |\n")
        f.write("|-----------|-----------------|\n")
        for item in knowledge_map:
            f.write(f"| `{item['path']}` | {item['snippet'][:150]}... |\n")

    print(f"✅ Map saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    index_omega()
