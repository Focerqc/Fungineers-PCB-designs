import json
from collections import Counter
from pathlib import Path

d = json.loads(Path("qfbms32 ai pcb/qfbms32_erc.json").read_text(encoding="utf-8"))
for want in ("unconnected_wire_endpoint", "label_dangling", "multiple_net_names", "label_multiple_wires"):
    print(f"\n=== {want} ===")
    n = 0
    for s in d["sheets"]:
        for v in s.get("violations", []):
            if v.get("type") != want:
                continue
            n += 1
            if n <= 6:
                print(v.get("description", ""))
                for it in v.get("items", []):
                    print(" ", it.get("description", "")[:100], it.get("pos"))
    print("count", n)

# BQ VC still NC
print("\n=== remaining BQ VC NC ===")
for s in d["sheets"]:
    for v in s.get("violations", []):
        if v.get("type") != "pin_not_connected":
            continue
        desc = v.get("items", [{}])[0].get("description", "")
        if "U_BQ" in desc and "VC" in desc:
            print(desc)
