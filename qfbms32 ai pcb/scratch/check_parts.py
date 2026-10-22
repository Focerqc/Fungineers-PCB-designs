import re
import os

with open('VFBMS32.kicad_sch', 'r', encoding='utf-8') as f:
    text_sch = f.read()

refs_sch = re.findall(r'\(property "Reference" "([^"]+)"', text_sch)
print("Schematic refs count:", len(refs_sch))
print("Capacitors in sch:", [r for r in refs_sch if r.startswith('C')])
print("Diodes in sch:", [r for r in refs_sch if r.startswith('D')])
print("Power/Misc in sch:", [r for r in refs_sch if not r.startswith('R_B') and not r.startswith('R_F') and not r.startswith('C_B')])

with open('VFBMS32.kicad_pcb', 'r', encoding='utf-8') as f:
    text_pcb = f.read()

# Let's inspect C_FLT1 footprint definition in kicad_pcb
match = re.search(r'\((?:footprint|module)\s+"([^"]+)"[^\)]*?\(at\s+([0-9\.\-]+)\s+([0-9\.\-]+)(?:\s+([0-9\.\-]+))?\).*?\(property\s+"Reference"\s+"C_FLT1".*?\n\t\)', text_pcb, re.DOTALL)
if not match:
    # try another regex
    pos = text_pcb.find('"C_FLT1"')
    if pos != -1:
        start = text_pcb.rfind('(footprint', 0, pos)
        end = text_pcb.find('(footprint', pos)
        print("C_FLT1 PCB section:")
        print(text_pcb[start:start+1200])
