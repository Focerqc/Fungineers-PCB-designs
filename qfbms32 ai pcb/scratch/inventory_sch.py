"""Inventory schematic parts and wiring stats."""
import re
from pathlib import Path

sch_path = Path(__file__).resolve().parents[1] / "qfbms32.kicad_sch"
sch = sch_path.read_text(encoding="utf-8")
print("wire", len(re.findall(r"\(wire\b", sch)))
print("label", len(re.findall(r"\(label\b", sch)))
print("junction", len(re.findall(r"\(junction\b", sch)))
print("global_label", len(re.findall(r"\(global_label\b", sch)))
print("power lib_id", len(re.findall(r'lib_id "power:', sch)))

# Parse symbol instances (top-level, not lib defs): after (symbol (lib_id ...
# Lib defs are inside (lib_symbols ...); instances are later.
lib_end = sch.find("(lib_symbols")
# Find closing of lib_symbols is hard; instead find instances by looking for
# (symbol (lib_id that appear with (at X Y
inst_pat = re.compile(
    r'\(symbol \(lib_id "([^"]+)"\s*\(at ([0-9.-]+) ([0-9.-]+) ([0-9.-]+)\)'
    r'(.*?)\n\t\)',
    re.S,
)
refs = []
for m in inst_pat.finditer(sch):
    lib, x, y, rot, body = m.groups()
    rm = re.search(r'\(property "Reference" "([^"]+)"', body)
    vm = re.search(r'\(property "Value" "([^"]+)"', body)
    fm = re.search(r'\(property "Footprint" "([^"]+)"', body)
    if not rm:
        continue
    refs.append(
        (
            rm.group(1),
            vm.group(1) if vm else "",
            fm.group(1) if fm else "",
            lib,
            float(x),
            float(y),
        )
    )

print("instances", len(refs))
keys = (
    "U_BQ",
    "C_",
    "R_F",
    "R_B",
    "J_CELL",
    "J_BAT",
    "J_CHG",
    "U_SSR",
    "R_SSR",
    "D_GS",
    "R_G",
    "R_GS",
    "Q",
    "U_ESP",
    "U4",
    "U7",
)
for r, v, fp, lib, x, y in sorted(refs):
    if any(r.startswith(k) for k in keys) or r in ("Q1", "Q2", "F1", "L1"):
        print(f"{r:10} {v:22} @({x:6.1f},{y:6.1f}) {fp}")
