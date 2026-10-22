import re

with open('VFBMS32.kicad_sch', 'r', encoding='utf-8') as f:
    sch = f.read()

with open('VFBMS32.kicad_pcb', 'r', encoding='utf-8') as f:
    pcb = f.read()

print("--- ALL SCHEMATIC SYMBOLS ---")
for m in re.finditer(r'\(symbol\s+\(lib_id\s+"([^"]+)"\)([\s\S]*?\n\t\))', sch):
    lib_id = m.group(1)
    body = m.group(2)
    ref = re.search(r'\(property "Reference" "([^"]+)"', body)
    val = re.search(r'\(property "Value" "([^"]+)"', body)
    fp = re.search(r'\(property "Footprint" "([^"]+)"', body)
    at = re.search(r'\(at\s+([0-9\.\-]+)\s+([0-9\.\-]+)', body)
    ref_s = ref.group(1) if ref else '?'
    val_s = val.group(1) if val else '?'
    fp_s = fp.group(1) if fp else '?'
    at_s = f"({at.group(1)}, {at.group(2)})" if at else '?'
    print(f"{ref_s:<10} | {val_s:<35} | at {at_s:<15} | lib: {lib_id}")

print("\n--- ALL SCHEMATIC LABELS / NETS ---")
labels = re.findall(r'\((?:label|global_label|hierarchical_label)\s+"([^"]+)"\s+\(at\s+([0-9\.\-]+)\s+([0-9\.\-]+)', sch)
for lab, x, y in labels:
    print(f"Label: {lab:<20} at ({x}, {y})")

print("\n--- ALL PCB FOOTPRINTS ---")
for m in re.finditer(r'\(footprint\s+"([^"]+)"([\s\S]*?\n\t\))', pcb):
    fp_name = m.group(1)
    body = m.group(2)
    ref = re.search(r'\(property "Reference" "([^"]+)"', body)
    val = re.search(r'\(property "Value" "([^"]+)"', body)
    at = re.search(r'\(at\s+([0-9\.\-]+)\s+([0-9\.\-]+)(?:\s+([0-9\.\-]+))?\)', body)
    ref_s = ref.group(1) if ref else '?'
    val_s = val.group(1) if val else '?'
    rot = at.group(3) if at and at.group(3) else '0'
    at_s = f"({at.group(1)}, {at.group(2)}, rot={rot})" if at else '?'
    print(f"{ref_s:<10} | {val_s:<25} | at {at_s:<25} | fp: {fp_name}")
