#!/data/data/com.termux/files/usr/bin/env python3
import os, hashlib, json

ROOT = os.path.expanduser("~/UNIFIED_ENGINE")

hashes = {}
dupes = []

for base, dirs, files in os.walk(ROOT):
    for f in files:
        path = os.path.join(base, f)
        try:
            with open(path, 'rb') as fp:
                data = fp.read()
            md5 = hashlib.md5(data).hexdigest()

            if md5 in hashes:
                dupes.append(path)
            else:
                hashes[md5] = path
        except:
            continue

# remove duplicates
for d in dupes:
    try:
        os.remove(d)
    except:
        pass

# write report
report = os.path.expanduser("~/UNIFIED_ENGINE/OPTIMIZER/dedupe_report.json")
with open(report, "w") as f:
    json.dump({"kept": hashes, "removed": dupes}, f, indent=2)

print("DEDUP DONE. Report:", report)
