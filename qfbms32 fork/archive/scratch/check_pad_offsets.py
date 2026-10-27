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

for target in ["J_CELL1", "R_B20", "R_F20"]:
    txt = fps[target]
    print(f"=== {target} ===")
    pads = re.findall(r'\(pad\s+"([^"]*)"\s+([^\s]+)\s+([^\s]+)\s+\(at\s+([0-9\.\-]+)\s+([0-9\.\-]+)', txt)
    for p in pads:
        print(f"  Pad {p[0]:4} at local ({float(p[3]):.2f}, {float(p[4]):.2f})")
