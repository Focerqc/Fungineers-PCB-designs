with open(r"c:\Users\quinn\Desktop\AI PCB CAD\Q VFBMS32 AI PCB\_reference\Meh ASM vbms STEP FILE.STEP", "r", errors="ignore") as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if any(k in line for k in ["XT30PW-F", "XT30PW-M", "real-ish vfbms32"]):
        print(f"Line {i+1}: {line.strip()[:100]}")
        for j in range(max(0, i-5), min(len(lines), i+15)):
            if "AXIS2_PLACEMENT_3D" in lines[j] or "CARTESIAN_POINT" in lines[j]:
                print(f"  [{j+1}] {lines[j].strip()}")
