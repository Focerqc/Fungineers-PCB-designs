with open('VFBMS32.kicad_sch', 'r', encoding='utf-8') as f:
    text = f.read()

import re

# Match each symbol block
# In KiCad sch, symbols after lib_symbols:
# (symbol (lib_id ...) (at x y rot) ... (property "Reference" "...") (property "Value" "...") (property "Footprint" "..."))
symbol_matches = re.findall(r'\(symbol\s+\(lib_id\s+"([^"]+)"\)\s+\(at\s+([0-9\.\-]+)\s+([0-9\.\-]+)(?:\s+([0-9\.\-]+))?\).*?\(property\s+"Reference"\s+"([^"]+)".*?\(property\s+"Value"\s+"([^"]+)".*?\(property\s+"Footprint"\s+"([^"]*)"', text, re.DOTALL)
print(f"Matched {len(symbol_matches)} schematic components:")
for lib_id, x, y, rot, ref, val, fp in symbol_matches:
    print(f"{ref:10s} | {val:25s} | at ({float(x):6.2f}, {float(y):6.2f}) | {lib_id} | {fp}")
