import re
from pathlib import Path

sch = Path("qfbms32 ai pcb/qfbms32.kicad_sch").read_text(encoding="utf-8")
# Find instance U_BQ1 at
m = re.search(
    r'\(lib_id "Battery_Management:BQ7695202PFB"\)\s*\(at ([0-9.-]+) ([0-9.-]+) ([0-9.-]+)\)[\s\S]*?'
    r'\(property "Reference" "U_BQ1"',
    sch,
)
print("U_BQ1 at", m.groups() if m else None)

# Extract pin 15 from lib
lib = re.search(
    r'\(symbol "Battery_Management:BQ7695202PFB"([\s\S]*?)\n\t\t\)\n\t\t\(symbol "Battery_Management:BQ7695202PFB_',
    sch,
)
# simpler: find pin number 15 in lib
for pnum in ("15", "16", "48", "12", "8"):
    # pin blocks contain number "15"
    pat = rf'\(pin \w+ line\s*\(at ([0-9.-]+) ([0-9.-]+) ([0-9.-]+)\)\s*\(length [0-9.]+\)[\s\S]*?\(number "{pnum}"'
    pm = re.search(pat, sch)
    if pm:
        print(f"pin {pnum} at rel", pm.groups())
        if m:
            sx, sy = float(m.group(1)), float(m.group(2))
            print(f"  abs", sx + float(pm.group(1)), sy + float(pm.group(2)))

# Check which VC pins are NOT in pin_not_connected - infer connected
import json
d = json.loads(Path("qfbms32 ai pcb/qfbms32_erc.json").read_text(encoding="utf-8"))
nc = set()
for s in d["sheets"]:
    for v in s.get("violations", []):
        if v.get("type") != "pin_not_connected":
            continue
        desc = v.get("items", [{}])[0].get("description", "")
        if "U_BQ1" in desc:
            mm = re.search(r"Pin (\d+|D) \[(\w+)", desc)
            if mm:
                nc.add((mm.group(1), mm.group(2)))
print("U_BQ1 NC pins", sorted(nc, key=lambda t: t[0]))
# expected VC pins
all_vc = [("48", "VC16"), ("15", "VC1"), ("16", "VC0"), ("17", "VSS"), ("18", "SRP"), ("20", "SRN")]
print("sample expected connected?", "16" not in {p for p,_ in nc})
