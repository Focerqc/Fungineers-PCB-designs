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
            val_m = re.search(r'\(property "Value" "([^"]+)"', txt)
            pos_m = re.search(r'\(at\s+([0-9\.\-]+)\s+([0-9\.\-]+)(?:\s+([0-9\.\-]+))?\)', txt)
            fp_type_m = re.search(r'\(footprint\s+"([^"]+)"', txt)
            if ref_m and pos_m:
                ref = ref_m.group(1)
                val = val_m.group(1) if val_m else ""
                fp_type = fp_type_m.group(1) if fp_type_m else ""
                x = float(pos_m.group(1))
                y = float(pos_m.group(2))
                rot = float(pos_m.group(3)) if pos_m.group(3) else 0.0
                fps.append((ref, val, fp_type, x, y, rot))

print(f"Total footprints: {len(fps)}")
bottom_comps = [fp for fp in fps if fp[4] >= 20.0 and not fp[0] in ["Q1", "Q2", "J_BAT1", "J_CHG1"]]
print(f"Bottom row components ({len(bottom_comps)}):")
for ref, val, fp_type, x, y, rot in sorted(bottom_comps, key=lambda item: (item[4], item[3])):
    print(f"  {ref:12} | {val:15} | {fp_type:35} | at ({x:6.2f}, {y:6.2f}, rot={rot:5.1f})")
