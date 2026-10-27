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

print(f"Total footprints in PCB: {len(footprints)}")
for fp, x, y, rot, ref, val in sorted(footprints, key=lambda f: f[4]):
    print(f"{ref:12} {val:20} at ({float(x):6.2f}, {float(y):6.2f}) rot={rot}  fp={fp}")
