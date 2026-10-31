"""List all schematic symbol instances with positions."""
from __future__ import annotations

import re
from pathlib import Path

SCH = Path(__file__).resolve().parents[1] / "qfbms32.kicad_sch"
sch = SCH.read_text(encoding="utf-8")

# Match both compact and multiline instance forms after lib_symbols.
# Strategy: find each '(symbol' that has lib_id as first child (instance), not nested def.
# Instances appear as top-level tabs: \t(symbol\n\t\t(lib_id OR \t(symbol (lib_id

pat = re.compile(
    r'\n\t\(symbol\s*(?:\n\t\t|\s+)\(lib_id\s+"([^"]+)"'
    r"(?:.*?\n\t\t|\s+)\(at\s+([0-9.-]+)\s+([0-9.-]+)\s+([0-9.-]+)\)"
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
for r, v, lib, x, y, rot in sorted(refs, key=lambda t: t[0]):
    print(f"{r:12} {v:28} @({x:7.2f},{y:7.2f}) r={rot:g} {lib}")

# Also check for floating labels positions
print("\n--- labels ---")
for m in re.finditer(
    r'\(label\s+"([^"]+)"\s*\(at\s+([0-9.-]+)\s+([0-9.-]+)\s+([0-9.-]+)\)',
    sch,
):
    print(f"  {m.group(1):16} @({float(m.group(2)):.2f},{float(m.group(3)):.2f}) rot={m.group(4)}")
