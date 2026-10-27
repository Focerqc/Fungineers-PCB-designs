import re

with open('qfbms32.kicad_sch', 'r', encoding='utf-8') as f:
    sch = f.read()

symbols = re.findall(r'\(symbol\s+\(lib_id\s+"([^"]+)".*?\(at\s+([\d\.-]+)\s+([\d\.-]+)(?:\s+([\d\.-]+))?\).*?\(property\s+"Reference"\s+"([^"]+)".*?\(property\s+"Value"\s+"([^"]+)"', sch, re.DOTALL)

print(f"Total symbols found: {len(symbols)}")
for lib_id, x, y, rot, ref, val in sorted(symbols, key=lambda s: s[4]):
    print(f"{ref:12} {val:20} at ({float(x):6.2f}, {float(y):6.2f})  lib={lib_id}")
