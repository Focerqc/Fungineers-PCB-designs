with open("VFBMS32.kicad_sch", "r", encoding="utf-8") as f:
    text = f.read()

import re
wires = re.findall(r'\(wire\s+\(pts\s+\(xy\s+([0-9\.\-]+)\s+([0-9\.\-]+)\)\s+\(xy\s+([0-9\.\-]+)\s+([0-9\.\-]+)\)\)', text)
for x1, y1, x2, y2 in wires:
    if 160 <= float(x1) <= 230 and 90 <= float(y1) <= 130:
        print(f"Wire ({x1}, {y1}) -> ({x2}, {y2})")
