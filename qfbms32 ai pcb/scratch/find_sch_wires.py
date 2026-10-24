import re

with open('qfbms32.kicad_sch', 'r', encoding='utf-8') as f:
    sch = f.read()

# Let's find wires near (140-210, 20-90)
wires = re.findall(r'\(wire\s+\(pts\s+\(xy\s+([\d\.-]+)\s+([\d\.-]+)\)\s+\(xy\s+([\d\.-]+)\s+([\d\.-]+)\)\)\)', sch)
labels = re.findall(r'\((?:hierarchical_)?label\s+"([^"]+)"\s+\(at\s+([\d\.-]+)\s+([\d\.-]+)', sch)

print("Labels in schematic:")
for l, x, y in labels:
    print(f"  {l:20} at ({float(x):6.2f}, {float(y):6.2f})")
