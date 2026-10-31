"""Compare PCB footprint refs vs schematic instances."""
from __future__ import annotations

import re
from collections import Counter
from pathlib import Path

import pcbnew

ROOT = Path(__file__).resolve().parents[1]
board = pcbnew.LoadBoard(str(ROOT / "qfbms32.kicad_pcb"))
pcb_refs = sorted(fp.GetReference() for fp in board.GetFootprints())
print("PCB footprints", len(pcb_refs))

sch = (ROOT / "qfbms32.kicad_sch").read_text(encoding="utf-8")
sch_inst = []
pat = re.compile(
    r'\n\t\(symbol\s*(?:\n\t\t|\s+)\(lib_id\s+"([^"]+)"'
    r"(?:.*?\n\t\t|\s+)\(at\s+([0-9.-]+)\s+([0-9.-]+)\s+([0-9.-]+)\)"
    r"(.*?)\n\t\)",
    re.S,
)
for m in pat.finditer(sch):
    rm = re.search(r'\(property\s+"Reference"\s+"([^"]+)"', m.group(5))
    if rm:
        sch_inst.append(rm.group(1))
print("SCH instances", len(sch_inst), sorted(sch_inst))

missing = [r for r in pcb_refs if r not in sch_inst]
extra = [r for r in sch_inst if r not in pcb_refs]
print("On PCB not in SCH", len(missing))
c = Counter()
for r in missing:
    if r.startswith("R_F"):
        prefix = "R_F*"
    elif r.startswith("R_B"):
        prefix = "R_B*"
    elif r.startswith("C_F"):
        prefix = "C_F*"
    elif r.startswith("C_B"):
        prefix = "C_B*"
    elif r.startswith("J_CELL"):
        prefix = "J_CELL*"
    elif r.startswith("J_T"):
        prefix = "J_T*"
    else:
        prefix = re.sub(r"\d+$", "*", r)
    c[prefix] += 1
for k, v in sorted(c.items()):
    print(f"  {k}: {v}")
print("extra on SCH not PCB:", extra)
print("other missing sample:", [r for r in missing if not r.startswith(("R_F", "R_B", "C_F", "C_B"))])
