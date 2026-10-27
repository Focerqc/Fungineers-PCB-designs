import re

with open('qfbms32.kicad_sch', 'r', encoding='utf-8') as f:
    text = f.read()

refs = re.findall(r'\(property "Reference" "([^"]+)"', text)
print("Schematic refs with R:", [r for r in refs if "R" in r])
