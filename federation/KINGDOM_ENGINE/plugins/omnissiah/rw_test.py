import json
import os
from datetime import datetime

test_path = os.path.expanduser("~/Omnissiah_Workspace/rw_test.json")

# WRITE TEST
data = {"test": "OK", "timestamp": str(datetime.now())}
with open(test_path, "w") as f:
    json.dump(data, f)

# READ TEST
with open(test_path, "r") as f:
    loaded = json.load(f)

print("WRITE_OK" if data["test"] == "OK" else "WRITE_FAIL")
print("READ_OK" if loaded["test"] == "OK" else "READ_FAIL")
print("FILE:", test_path)
print("DATA:", loaded)
