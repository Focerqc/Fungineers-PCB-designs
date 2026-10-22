import re

with open(r'c:\Users\quinn\Desktop\AI PCB CAD\Q VFBMS32 AI PCB\build_vfbms32_layout.py', 'r') as f:
    text = f.read()

comps = re.findall(r'\{\s*"dir":.*?"ref":\s*"([^"]+)".*?"val":\s*"([^"]+)".*?"x":\s*([-\d.]+).*?"y":\s*([-\d.]+)', text, re.DOTALL)
for c in comps:
    print(f"{c[0]:15} {c[1]:20} ({c[2]}, {c[3]})")
