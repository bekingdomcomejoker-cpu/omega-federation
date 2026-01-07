import os, json

ROOT = "/data/data/com.termux/files/home/KINGDOM_ENGINE"

def build_index():
    paths = {}
    for base, dirs, files in os.walk(ROOT):
        for f in files:
            full = os.path.join(base, f)
            try:
                size = os.path.getsize(full)
            except:
                size = None
            paths[full] = {"size": size}
    with open(os.path.join(ROOT, "context_index.json"), "w") as fp:
        json.dump(paths, fp, indent=2)

if __name__ == "__main__":
    build_index()
    print("[✓] context_index.json updated.")
