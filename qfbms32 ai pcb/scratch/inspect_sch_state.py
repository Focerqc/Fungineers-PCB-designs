"""Inspect schematic symbol instances, pin positions, and connectivity readiness."""
from __future__ import annotations

import re
import uuid
from pathlib import Path

SCH = Path(__file__).resolve().parents[1] / "qfbms32.kicad_sch"
sch = SCH.read_text(encoding="utf-8")

print("size", len(sch), "lines", sch.count("\n"))
print("wire", len(re.findall(r"\(wire\b", sch)))
print("label", len(re.findall(r"\(label\b", sch)))
print("global_label", len(re.findall(r"\(global_label\b", sch)))
print("junction", len(re.findall(r"\(junction\b", sch)))
print("symbol(lib_id", len(re.findall(r"\(symbol\s+\(lib_id", sch)))

# Find symbol instances: after lib_symbols section. Match (symbol (lib_id ... (at
pat = re.compile(
    r'\(symbol\s+\(lib_id\s+"([^"]+)"\s*'
    r"\(at\s+([0-9.-]+)\s+([0-9.-]+)\s+([0-9.-]+)\)"
    r"(.*?)\n\t\)",
    re.S,
)
refs = []
for m in pat.finditer(sch):
    lib, x, y, rot, body = m.groups()
    rm = re.search(r'\(property\s+"Reference"\s+"([^"]+)"', body)
    vm = re.search(r'\(property\s+"Value"\s+"([^"]+)"', body)
    if not rm:
        continue
    refs.append((rm.group(1), vm.group(1) if vm else "", lib, float(x), float(y), float(rot)))

print("instances", len(refs))
keys = (
    "U_BQ",
    "U_SSR",
    "U_ESP",
    "U3",
    "U4",
    "U7",
    "J_CELL",
    "J_BAT",
    "J_CHG",
    "J_COMM",
    "J_T",
    "J_USB",
    "R_F",
    "R_B",
    "C_F",
    "C_SSR",
    "Q1",
    "Q2",
    "F1",
    "R_SH",
    "R_SSR",
    "R_G",
    "D_GS",
)
for r, v, lib, x, y, rot in sorted(refs, key=lambda t: (t[0], t[3])):
    if any(r.startswith(k) for k in keys) or r in ("Q1", "Q2", "F1", "L1"):
        print(f"{r:10} {v:22} @({x:7.2f},{y:7.2f}) rot={rot:g} {lib}")

# Dump BQ pin defs from lib_symbols
print("\n--- BQ symbol pin numbers in lib ---")
# Find first BQ76952 lib symbol block briefly
for name in ("BQ76952", "bq76952", "BQ7695202"):
    if name in sch:
        print("found string", name)

# Extract pin (number ...) from first U_BQ-related lib
lib_m = re.search(
    r'\(symbol\s+"([^"]*[Bb][Qq]76952[^"]*)"(.*?)\)\n\t\)',
    sch,
    re.S,
)
if lib_m:
    print("lib symbol", lib_m.group(1))
    pins = re.findall(
        r'\(pin\s+(\w+)\s+line\s*\(at\s+([0-9.-]+)\s+([0-9.-]+)\s+([0-9.-]+)\).*?'
        r'\(name\s+"([^"]+)".*?\(number\s+"([^"]+)"',
        lib_m.group(2),
        re.S,
    )
    for etype, px, py, prot, pname, pnum in pins:
        print(f"  pin {pnum:>3} {pname:12} @({px},{py}) rot={prot} {etype}")
else:
    print("no BQ lib match; listing lib_symbol names with BQ/U")
    for m in re.finditer(r'\(symbol\s+"([^"]+)"', sch):
        n = m.group(1)
        if "BQ" in n.upper() or "76952" in n or n.startswith("qfbms"):
            print(" ", n)
