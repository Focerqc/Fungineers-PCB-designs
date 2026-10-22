with open('build_vfbms32_layout.py', 'r', encoding='utf-8') as f:
    code = f.read()

import re
refs_script = re.findall(r'"ref":\s*"([^"]+)"', code)
print("Refs in build_vfbms32_layout.py:", refs_script)

with open('VFBMS32.kicad_pcb', 'r', encoding='utf-8') as f:
    pcb = f.read()

refs_pcb = re.findall(r'\(property "Reference" "([^"]+)"', pcb)
print(f"Total refs in PCB: {len(refs_pcb)}")
print("Non-resistor/cap refs in PCB:", [r for r in refs_pcb if not r.startswith('R_B') and not r.startswith('R_F')])
