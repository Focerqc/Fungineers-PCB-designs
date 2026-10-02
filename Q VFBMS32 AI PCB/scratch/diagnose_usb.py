import os
import re

pcb_path = r"c:\Users\quinn\Documents\GitHub\Fungineers PCB designs\Q VFBMS32 AI PCB\VFBMS32.kicad_pcb"
with open(pcb_path, "r", encoding="utf-8") as f:
    lines = f.readlines()

in_fp = False
curr_fp = []
depth = 0
fps = {}

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
            if ref_m:
                ref = ref_m.group(1)
                fps[ref] = txt

print("Found footprints count:", len(fps))
for target in ["J_USB1", "U7", "U_ESP1", "BZ1"]:
    if target in fps:
        print(f"\n=================== {target} ===================")
        fp_str = fps[target]
        print(fp_str[:2000])
        # count pads
        pads = re.findall(r'\(pad\s+"([^"]+)"\s+([^\s]+)', fp_str)
        print(f"Total pads in {target}: {len(pads)}")
        for p in pads:
            print(f"  Pad {p[0]}: type {p[1]}")
    else:
        print(f"\n{target} NOT found in PCB!")
