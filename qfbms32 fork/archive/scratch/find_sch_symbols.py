import re

with open('qfbms32.kicad_sch', 'r', encoding='utf-8') as f:
    sch = f.read()

symbols = re.findall(r'\(symbol\s+\(lib_id\s+"([^"]+)".*?\(at\s+([\d\.-]+)\s+([\d\.-]+)(?:\s+([\d\.-]+))?\).*?\(property\s+"Reference"\s+"([^"]+)".*?\(property\s+"Value"\s+"([^"]+)"', sch, re.DOTALL)

for lib_id, x, y, rot, ref, val in symbols:
    x, y = float(x), float(y)
    if 130 <= x <= 220 and 0 <= y <= 100:
        print(f"{ref:12} {val:15} at ({x:6.2f}, {y:6.2f})  lib={lib_id}")
