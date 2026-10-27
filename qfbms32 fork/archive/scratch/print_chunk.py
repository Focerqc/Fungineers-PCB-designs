with open("VFBMS32.kicad_pcb", "r", encoding="utf-8") as f:
    text = f.read()

import re

for ref in ["C_FLT1", "R_SH1"]:
    pos = text.find(f'"{ref}"')
    if pos != -1:
        start = text.rfind('(footprint', 0, pos)
        end = text.find('(footprint', pos)
        print(f"=== {ref} ===")
        print(text[start:end])
