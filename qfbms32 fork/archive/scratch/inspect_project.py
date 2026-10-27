import os
import re

with open('VFBMS32.kicad_sch', 'r', encoding='utf-8') as f:
    sch_text = f.read()

with open('VFBMS32.kicad_pcb', 'r', encoding='utf-8') as f:
    pcb_text = f.read()

print("=== SCHEMATIC SYMBOL INSTANCES ===")
for m in re.finditer(r'\(symbol\s+\(lib_id\s+"([^"]+)"\)([\s\S]*?)\n\t\)', sch_text):
    lib_id = m.group(1)
    body = m.group(2)
    ref = re.search(r'\(property "Reference" "([^"]+)"', body)
    val = re.search(r'\(property "Value" "([^"]+)"', body)
    fp = re.search(r'\(property "Footprint" "([^"]+)"', body)
    print(f"Ref: {ref.group(1) if ref else '?':<12} | Val: {val.group(1) if val else '?':<30} | Lib: {lib_id:<35} | FP: {fp.group(1) if fp else '?'}")

print("\n=== PCB FOOTPRINTS ===")
for m in re.finditer(r'\(footprint\s+"([^"]+)"([\s\S]*?)\n\t\)', pcb_text):
    fp_name = m.group(1)
    body = m.group(2)
    ref = re.search(r'\(property "Reference" "([^"]+)"', body)
    val = re.search(r'\(property "Value" "([^"]+)"', body)
    at = re.search(r'\(at\s+([0-9\.\-]+)\s+([0-9\.\-]+)(?:\s+([0-9\.\-]+))?\)', body)
    pos = f"({at.group(1)}, {at.group(2)}, rot={at.group(3) if at.group(3) else '0'})" if at else "?"
    if ref and ref.group(1) in ['L2', 'U7', 'J_USB1', 'U6', 'U1', 'U2', 'U_ESP1', 'U_CAN1']:
        print(f"Ref: {ref.group(1):<12} | Val: {val.group(1) if val else '?':<20} | Pos: {pos:<30} | Footprint: {fp_name}")
