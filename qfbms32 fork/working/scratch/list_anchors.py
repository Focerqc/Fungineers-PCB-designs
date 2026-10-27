"""List IC / connector / power-stage anchors on the working PCB."""
import re
from pathlib import Path

pcb = Path(__file__).resolve().parents[1] / "qfbms32.kicad_pcb"
text = pcb.read_text(encoding="utf-8", errors="replace")

# Split on footprint blocks (KiCad s-expr)
pat = re.compile(
    r'\(footprint "([^"]+)"(.*?)\n\t\)',
    re.DOTALL,
)

anchor_re = re.compile(
    r"^(U\d*|U_SSR\d*|J_|P_|SW|USB|XT|CN|BZ|F_|Q\d*|D_GS|D_CHG|SSR|H2440|CTAN|C_BULK)"
)

rows = []
for m in pat.finditer(text):
    fp, body = m.group(1), m.group(2)
    ref_m = re.search(r'\(property "Reference" "([^"]+)"', body)
    val_m = re.search(r'\(property "Value" "([^"]+)"', body)
    at_m = re.search(r"\(at ([-\d.]+) ([-\d.]+)(?: ([-\d.]+))?\)", body)
    if not ref_m or not at_m:
        continue
    ref = ref_m.group(1)
    if not anchor_re.match(ref) and not ref.startswith(("J_", "U", "Q", "XT", "USB", "BZ", "F_")):
        continue
    x, y = float(at_m.group(1)), float(at_m.group(2))
    rot = float(at_m.group(3) or 0)
    val = val_m.group(1) if val_m else ""
    short = fp.split(":")[-1] if ":" in fp else fp
    rows.append((ref, val, x, y, rot, short))

rows.sort(key=lambda r: (r[0][0], r[0]))
print(f"anchors: {len(rows)}")
for ref, val, x, y, rot, short in rows:
    print(f"{ref:12} {x:7.2f},{y:7.2f} r{rot:6.1f}  {val[:28]:28} {short[:45]}")
