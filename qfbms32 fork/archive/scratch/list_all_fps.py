import os
import re

pcb_path = r"c:\Users\quinn\Documents\GitHub\Fungineers PCB designs\Q VFBMS32 AI PCB\VFBMS32.kicad_pcb"
with open(pcb_path, "r", encoding="utf-8") as f:
    lines = f.readlines()

in_fp = False
curr_fp = []
depth = 0
fps = []

for line in lines:
    if line.strip().startswith("(footprint ") and depth == 0:
        in_fp = True
        depth = 1
        curr_fp = [line]
    elif in_fp:
        curr_fp.append(line)
        depth += line.count("(") - line.count(")")
        if depth == 0:
            in_fp = False
            txt = "".join(curr_fp)
            ref_m = re.search(r'\(property "Reference" "([^"]+)"', txt)
            pos_m = re.search(r'\(at\s+([0-9\.\-]+)\s+([0-9\.\-]+)(?:\s+([0-9\.\-]+))?\)', txt)
            if ref_m and pos_m:
                ref = ref_m.group(1)
                x = float(pos_m.group(1))
                y = float(pos_m.group(2))
                rot = float(pos_m.group(3)) if pos_m.group(3) else 0.0
                fps.append((ref, x, y, rot))

print("All footprints:")
for ref, x, y, rot in sorted(fps, key=lambda item: item[0]):
    print(f"{ref:15} at ({x:6.2f}, {y:6.2f}, rot={rot:5.1f})")
