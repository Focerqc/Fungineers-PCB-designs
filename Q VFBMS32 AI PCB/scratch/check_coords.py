import re

# Check current coordinates in build_vfbms32_layout.py
with open(r'c:\Users\quinn\Desktop\AI PCB CAD\Q VFBMS32 AI PCB\build_vfbms32_layout.py', 'r') as f:
    text = f.read()

for comp in ['U_ESP1', 'J_USB1', 'U7', 'U_BQ1', 'J_CELL1']:
    m = re.search(r'\"ref\":\s*\"' + comp + r'\"[\s\S]*?\"x\":\s*([\d.]+),\s*\"y\":\s*([\d.]+)', text)
    if m:
        print(f"{comp}: x={m.group(1)}, y={m.group(2)}")
