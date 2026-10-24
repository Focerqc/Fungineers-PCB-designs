import re

sch_path = r"c:\Users\quinn\Documents\GitHub\Fungineers PCB designs\qfbms32 ai pcb\qfbms32.kicad_sch"
with open(sch_path, "r", encoding="utf-8") as f:
    sch = f.read()

# Match all symbols where Reference starts with R
symbols = re.findall(r'\(symbol\s+\(lib_id\s+"[^"]+".*?\(property\s+"Reference"\s+"(R[^"]*)".*?\(property\s+"Value"\s+"([^"]*)"', sch, re.DOTALL)
print(f"Total resistors in sch: {len(symbols)}")
res_dict = {}
for r, v in symbols:
    res_dict[r] = v

for r in sorted(res_dict.keys()):
    print(f"  {r:12s} val={res_dict[r]}")
