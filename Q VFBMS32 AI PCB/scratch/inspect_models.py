import re

with open('VFBMS32.kicad_pcb', 'r', encoding='utf-8') as f:
    pcb = f.read()

for ref in ['L1', 'L2', 'U7', 'U_ESP1', 'J_USB1', 'U_SSR1']:
    m = re.search(r'(\(footprint\s+"([^"]+)"[\s\S]*?\(property\s+"Reference"\s+"' + ref + r'"[\s\S]*?\n\t\))', pcb)
    if m:
        full_block = m.group(1)
        # Find model in block
        models = re.findall(r'\(model\s+"([^"]+)"', full_block)
        at = re.search(r'\(at\s+([0-9\.\-]+)\s+([0-9\.\-]+)(?:\s+([0-9\.\-]+))?\)', full_block)
        pos = f"({at.group(1)}, {at.group(2)}, rot={at.group(3) if at.group(3) else '0'})" if at else "?"
        print(f"=== {ref} ===")
        print(f"Footprint: {m.group(2)}")
        print(f"Position: {pos}")
        print(f"3D Models: {models}")
    else:
        print(f"=== {ref} NOT FOUND ===")
