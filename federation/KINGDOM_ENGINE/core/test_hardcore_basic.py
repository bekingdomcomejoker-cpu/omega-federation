#!/usr/bin/env python3
from TTE_HARDCORE_v1 import ResonanceEngine, Guardian
import json, sys, os
cfg = json.load(open("core/hardcore_config.json"))
eng = ResonanceEngine(cfg)
tests = [
  ("I love and forgive and help others", "truth"),
  ("Everyone always lies, obviously", "fact"),
  ("This is nonsense gibberish 123", "lie")
]
for txt, expect in tests:
    r = eng.purify(txt)
    print(txt, "=>", r["category"], r["score"], "expected", expect)
