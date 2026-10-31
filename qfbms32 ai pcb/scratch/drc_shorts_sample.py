import json
from pathlib import Path

d = json.loads(Path("qfbms32 ai pcb/qfbms32_drc_violations.json").read_text(encoding="utf-8"))
n = 0
for v in d.get("violations", []):
    if v.get("type") not in ("shorting_items", "tracks_crossing", "clearance"):
        continue
    n += 1
    if n <= 15:
        print(v.get("type"), v.get("description", "")[:120])
        for it in v.get("items", [])[:3]:
            print(" ", it.get("description", "")[:100], it.get("pos"))
print("shown", min(n, 15), "of matching")
