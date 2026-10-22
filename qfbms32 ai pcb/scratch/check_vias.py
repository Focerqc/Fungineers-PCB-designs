import os
import re

pcb_path = r"c:\Users\quinn\Documents\GitHub\Fungineers PCB designs\Q VFBMS32 AI PCB\VFBMS32.kicad_pcb"
with open(pcb_path, "r", encoding="utf-8") as f:
    text = f.read()

# check vias or test points
vias = re.findall(r'\(via\s+([^\)]+)\)', text)
print(f"Total vias: {len(vias)}")
vias_bottom = []
for v in vias:
    m = re.search(r'\(at\s+([0-9\.\-]+)\s+([0-9\.\-]+)\)', v)
    if m:
        x, y = float(m.group(1)), float(m.group(2))
        if y >= 20:
            vias_bottom.append((x, y, v))

print(f"Vias at Y >= 20 ({len(vias_bottom)}):")
for vb in vias_bottom[:20]:
    print(" ", vb[0], vb[1])
