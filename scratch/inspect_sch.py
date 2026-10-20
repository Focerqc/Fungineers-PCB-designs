import re

with open('Q VFBMS32 AI PCB/VFBMS32.kicad_sch', 'r', encoding='utf-8') as f:
    sch = f.read()

# Check what symbols are defined in lib_symbols
lib_symbols = re.findall(r'\(symbol "([^"]+)"', sch[:sch.find('(sheet_instances')])
print("Lib symbols defined:")
for s in lib_symbols:
    print(" ", s)
