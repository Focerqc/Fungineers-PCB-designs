import re

with open('qfbms32.kicad_pcb', 'r', encoding='utf-8') as f:
    pcb = f.read()

footprints = re.findall(
    r'\(footprint\s+"([^"]+)".*?'
    r'\(at\s+([\d\.-]+)\s+([\d\.-]+)(?:\s+([\d\.-]+))?\).*?'
    r'\(property\s+"Reference"\s+"([^"]+)".*?'
    r'\(property\s+"Value"\s+"([^"]+)"',
    pcb, re.DOTALL
)

print("Footprints near X=20-35, Y=0-15:")
for fp, x, y, rot, ref, val in footprints:
    x_val, y_val = float(x), float(y)
    if 20 <= x_val <= 38 and 0 <= y_val <= 15:
        print(f"Ref: {ref:10} Val: {val:15} At: ({x_val:6.2f}, {y_val:6.2f}) Rot: {rot} Fp: {fp}")
