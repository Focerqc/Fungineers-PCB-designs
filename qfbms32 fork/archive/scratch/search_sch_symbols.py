import re

sch_path = r"c:\Users\quinn\Documents\GitHub\Fungineers PCB designs\qfbms32 ai pcb\qfbms32.kicad_sch"
with open(sch_path, "r", encoding="utf-8") as f:
    sch = f.read()

# Let's find all symbols in the schematic
symbol_pattern = re.compile(r'\(symbol\s+\(lib_id\s+"([^"]+)"\).*?\(property\s+"Reference"\s+"([^"]+)".*?\(property\s+"Value"\s+"([^"]+)"', re.DOTALL)

print("Symbols in schematic:")
for m in symbol_pattern.finditer(sch):
    lib_id, ref, val = m.group(1), m.group(2), m.group(3)
    if any(k in ref for k in ["Q", "SSR", "DISC", "SEC", "R_G", "R_CHG", "R_DSG", "D_"]):
        print(f"Ref: {ref:10s} Val: {val:25s} Lib: {lib_id}")
