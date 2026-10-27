import pcbnew
import re

board = pcbnew.LoadBoard('qfbms32 ai pcb/qfbms32.kicad_pcb')
pcb_refs = set(str(fp.GetReference()) for fp in board.GetFootprints())

with open('qfbms32 ai pcb/qfbms32.kicad_sch', 'r', encoding='utf-8') as f:
    sch = f.read()

# Only match top-level component references
refs = re.findall(r'\(symbol\s+\(lib_id\s+"[^"]+".*?\(property\s+"Reference"\s+"([^"]+)".*?\(property\s+"Value"\s+"([^"]+)"', sch, re.DOTALL)

print('In schematic but NOT on PCB:')
for r, v in sorted(set(refs)):
    if r not in pcb_refs and not r.startswith('G#') and not r.startswith('#'):
        print(f"  {r:12s} val={v}")
