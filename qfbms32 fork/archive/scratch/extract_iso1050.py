import re

sym_file = r'C:\Program Files\KiCad\10.0\share\kicad\symbols\Interface_CAN_LIN.kicad_sym'
with open(sym_file, 'r', encoding='utf-8', errors='ignore') as f:
    text = f.read()

for m in re.finditer(r'\(symbol\s+"(ISO1050[^"]*)"([\s\S]*?\n  \))', text):
    name = m.group(1)
    body = m.group(0)
    print(f"=== Symbol: {name} ===")
    print(body[:1500])
    print("...\n")
