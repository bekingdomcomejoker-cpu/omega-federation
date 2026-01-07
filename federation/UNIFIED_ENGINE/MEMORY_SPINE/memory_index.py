#!/data/data/com.termux/files/usr/bin/env python3
import os, json, time
SD = os.path.expanduser('~/storage/external-1/UNIFIED_BACKUP')
out = os.path.expanduser('~/UNIFIED_ENGINE/MEMORY_SPINE/meta/index.json')
archives = []
if not os.path.isdir(SD):
    print("SD not mounted or missing:", SD)
    raise SystemExit(1)
for fname in os.listdir(SD):
    if fname.startswith('memory_') and fname.endswith('.tar.gz'):
        path = os.path.join(SD, fname)
        try:
            st = os.stat(path)
            archives.append({
                "name": fname,
                "size": st.st_size,
                "mtime": int(st.st_mtime),
                "iso_mtime": time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime(st.st_mtime))
            })
        except FileNotFoundError:
            continue
archives.sort(key=lambda x: x['mtime'], reverse=True)
with open(out, 'w') as f:
    json.dump({"archives": archives}, f, indent=2)
print("Wrote JSON index:", out)
