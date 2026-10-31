"""Print C_F / R_F / R_B positions and layers from the working board."""
import re
from pathlib import Path

text = Path(r"qfbms32 ai pcb/qfbms32.kicad_pcb").read_text(encoding="utf-8")
parts = re.split(r"\n\t\(footprint ", text)
rows = []
for p in parts[1:]:
    rm = re.search(r'\(property "Reference" "([^"]+)"', p)
    if not rm:
        continue
    ref = rm.group(1)
    if not re.match(r"^(C_F|R_F|R_B)\d+$", ref):
        continue
    am = re.search(r"\n\t\t\(at ([0-9.\-]+) ([0-9.\-]+)(?: ([0-9.\-]+))?\)", p)
    lm = re.search(r'\n\t\t\(layer "([^"]+)"\)', p)
    rows.append((ref, am.group(1), am.group(2), am.group(3) or "0", lm.group(1) if lm else "?"))

def key(r):
    m = re.match(r"([A-Z_]+)(\d+)", r[0])
    return (m.group(1), int(m.group(2)))

for ref, x, y, rot, layer in sorted(rows, key=key):
    if ref.startswith("C_F") and ref not in ("C_F1", "C_F16", "C_F17", "C_F32"):
        continue
    if ref.startswith("R_F") and ref not in ("R_F1", "R_F16", "R_F32"):
        continue
    print(f"{ref:8} {layer:6} at {x:>8} {y:>8} rot {rot}")
print("counts", sum(1 for r in rows if r[0].startswith("C_F")), "C_F",
      sum(1 for r in rows if r[0].startswith("R_F")), "R_F",
      sum(1 for r in rows if r[0].startswith("R_B")), "R_B")
