with open('VFBMS32.kicad_pcb', 'r', encoding='utf-8') as f:
    pcb = f.read()

import re

for ref in ['D_CHG1', 'D_CHG2', 'D_CHG3', 'R_SH1', 'J_CHG1', 'J_BAT1', 'C_FLT1']:
    pos = pcb.find(f'"{ref}"')
    if pos != -1:
        start = pcb.rfind('(footprint', 0, pos)
        end = pcb.find('(footprint', pos)
        fp_block = pcb[start:end] if end != -1 else pcb[start:]
        pads = re.findall(r'\(pad\s+"([^"]+)"[^\)]+?(?:\(net\s+([0-9]+)\s+"([^"]+)")?', fp_block)
        print(f"Ref {ref} pads: {pads}")
