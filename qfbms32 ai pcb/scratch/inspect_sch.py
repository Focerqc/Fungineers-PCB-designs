import re

with open('VFBMS32.kicad_sch', 'r', encoding='utf-8') as f:
    sch = f.read()

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
    print(f"{ref_s:<10} | {val_s:<35} | at {at_s:<15} | lib: {lib_id} | fp: {fp_s}")

print("\n--- SCHEMATIC WIRES ---")
wires = re.findall(r'\(wire\s+\(pts\s+\(xy\s+([0-9\.\-]+)\s+([0-9\.\-]+)\)\s+\(xy\s+([0-9\.\-]+)\s+([0-9\.\-]+)\)\)', sch)
print(f"Total wires: {len(wires)}")

print("\n--- SCHEMATIC LABELS ---")
for m in re.finditer(r'\((label|global_label|hierarchical_label)\s+"([^"]+)"[\s\S]*?\(at\s+([0-9\.\-]+)\s+([0-9\.\-]+)(?:\s+([0-9\.\-]+))?\)', sch):
    ltype, lab, x, y, rot = m.group(1), m.group(2), m.group(3), m.group(4), m.group(5) or '0'
    print(f"{ltype:<15} : {lab:<25} at ({x}, {y}, rot={rot})")
