import os
import json

archive_path = os.path.expanduser("~/KINGDOM_ENGINE")
memory_map = {}

for root, dirs, files in os.walk(archive_path):
    for file in files:
        if file.endswith((".txt", ".md", ".sh")):
            with open(os.path.join(root, file), 'r') as f:
                # Seizing the first 100 characters as a "Semantic Signature"
                memory_map[file] = f.read(100).replace("\n", " ")

with open(os.path.expanduser("~/wire_memory.json"), 'w') as f:
    json.dump(memory_map, f)
print("Memory Map Generated: ~/wire_memory.json")
