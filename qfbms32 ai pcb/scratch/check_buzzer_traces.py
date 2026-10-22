with open("VFBMS32.kicad_pcb", "r", encoding="utf-8") as f:
    text = f.read()

import re
segs = re.findall(r'\(segment\s+\(start ([-\d.]+) ([-\d.]+)\)\s+\(end ([-\d.]+) ([-\d.]+)\)\s+\(width ([-\d.]+)\)\s+\(layer "([^"]+)"\)\s+\(net (\d+)\)', text)
print("Segments near buzzer:")
for s in segs:
    x1, y1, x2, y2 = float(s[0]), float(s[1]), float(s[2]), float(s[3])
    if 84 <= x1 <= 94 and 0 <= y1 <= 8:
        print(s)

vias = re.findall(r'\(via\s+\(at ([-\d.]+) ([-\d.]+)\)\s+\(size ([-\d.]+)\)\s+\(drill ([-\d.]+)\).*?\(net (\d+)\)', text, re.DOTALL)
print("Vias near buzzer:")
for v in vias:
    x, y = float(v[0]), float(v[1])
    if 84 <= x <= 94 and 0 <= y <= 8:
        print(v)
