import os, re

filename = 'qfbms32.kicad_pcb' if os.path.exists('qfbms32.kicad_pcb') else 'qfbms32 ai pcb/qfbms32.kicad_pcb'

with open(filename, 'r', encoding='utf-8') as f:
    content = f.read()

pattern = re.compile(
    r'\(footprint\s+"([^"]+)".*?'
    r'\(at\s+([\d\.-]+)\s+([\d\.-]+)(?:\s+([\d\.-]+))?\).*?'
    r'\(property\s+"Reference"\s+"([^"]+)".*?'
    r'\(property\s+"Value"\s+"([^"]+)"',
    re.DOTALL
)

print(f"{'Ref':8} {'Value':15} {'X':>7} {'Y':>7} {'Rot':>6}  Footprint")
print("-" * 65)
for m in pattern.finditer(content):
    fp = m.group(1)
    x = float(m.group(2))
    y = float(m.group(3))
    rot = m.group(4) or "0"
    ref = m.group(5)
    val = m.group(6)
    if 20 <= x <= 45 and 0 <= y <= 12:
        print(f"{ref:8} {val:15} {x:7.2f} {y:7.2f} {rot:>6}  {fp}")
