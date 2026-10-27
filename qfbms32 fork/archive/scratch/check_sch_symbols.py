import os
import re

sch_path = r"c:\Users\quinn\Desktop\AI PCB CAD\Q VFBMS32 AI PCB\VFBMS32.kicad_sch"
with open(sch_path, "r", encoding="utf-8") as f:
    text = f.read()

symbols = re.findall(r'\(symbol\s+\(lib_id\s+\"([^\"]+)\"[\s\S]*?\(property\s+\"Reference\"\s+\"([^\"]+)\"[\s\S]*?\(property\s+\"Value\"\s+\"([^\"]+)\"', text)
print(f"Total symbols in schematic: {len(symbols)}")
for lib, ref, val in sorted(symbols, key=lambda x: x[1])[:30]:
    print(f"{ref}: {val} ({lib})")
