import json
import re
from collections import Counter
from pathlib import Path

d = json.loads(Path("qfbms32 ai pcb/qfbms32_erc.json").read_text(encoding="utf-8"))
bq_pin = Counter()
bq_lab = Counter()
for s in d["sheets"]:
    for v in s.get("violations", []):
        t = v.get("type")
        for it in v.get("items", []):
            desc = it.get("description", "")
            if "U_BQ" in desc and t:
                bq_pin[f"{t}|{desc}"] += 1
            if "Label" in desc and t in ("label_dangling", "isolated_pin_label"):
                bq_lab[f"{t}|{desc}"] += 1

print("--- BQ-related pin violations (sample) ---")
for k, n in sorted(bq_pin.items())[:40]:
    print(n, k)

print("\n--- dangling labels with BQ/CELL/VC ---")
for k, n in sorted(bq_lab.items()):
    if any(x in k for x in ("BQ", "CELL", "VC", "VBOOST", "CHG", "SSR", "TS", "SRP")):
        print(n, k)

# Count labels in sch at BQ1 VC1 location
sch = Path("qfbms32 ai pcb/qfbms32.kicad_sch").read_text(encoding="utf-8")
labs = re.findall(
    r'\(label "([^"]+)"\s*\(at ([0-9.-]+) ([0-9.-]+) ([0-9.-]+)\)',
    sch,
)
at_bq1 = [(n, x, y) for n, x, y, r in labs if abs(float(x) - 129.54) < 0.02]
print("\nlabels near x=129.54:", len(at_bq1))
for row in at_bq1[:20]:
    print(row)

# Check if BQ symbol pins need wires - maybe labels need to be global_label?
print("\nVC1 pin expected y", 100.33 + 2.54)
print([row for row in at_bq1 if "VC1" in row[0]])
