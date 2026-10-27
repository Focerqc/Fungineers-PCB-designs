with open("VFBMS32.kicad_pcb", "r", encoding="utf-8") as f:
    text = f.read()

import re

for ref in ["D_CHG1", "D_CHG2", "D_CHG3", "J_CHG1", "J_BAT1", "R_SH1", "Q1"]:
    pos = text.find(f'"{ref}"')
    if pos != -1:
        start = text.rfind('(footprint', 0, pos)
        end = text.find('(footprint', pos)
        chunk = text[start:end]
        pads = re.findall(r'\(pad\s+"([^"]+)".*?\(net\s+([0-9]+)\s+"([^"]+)"\)', chunk, re.DOTALL)
        print(f"=== {ref} ===")
        for p in pads:
            print(f"  pin {p[0]}: net {p[1]} ({p[2]})")
