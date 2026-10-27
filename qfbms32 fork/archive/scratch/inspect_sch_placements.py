import re

sch_path = r"c:\Users\quinn\Desktop\AI PCB CAD\Q VFBMS32 AI PCB\VFBMS32.kicad_sch"
with open(sch_path, "r", encoding="utf-8") as f:
    text = f.read()

# Let's inspect the instances of symbols in VFBMS32.kicad_sch
pattern = r'\(symbol\s+\(lib_id\s+\"([^\"]+)\"[\s\S]*?\(property\s+\"Reference\"\s+\"([^\"]+)\"[\s\S]*?\(at\s+([-\d.]+)\s+([-\d.]+)\s*([-\d.]*)\)[\s\S]*?\(property\s+\"Value\"\s+\"([^\"]+)\"'

# Let's search inside instantiated symbols
# Find all (symbol ... ) at top level
lines = text.splitlines()
symbols = []
curr = []
depth = 0
in_lib_symbols = False
for line in lines:
    if "(lib_symbols" in line:
        in_lib_symbols = True
    if in_lib_symbols:
        if line.strip() == ")": # check depth
            pass
    # simple matcher
for m in re.finditer(r'\(symbol\s+\(lib_id\s+\"([^\"]+)\"[\s\S]*?\n\t\)', text):
    sym_block = m.group(0)
    ref_m = re.search(r'\(property\s+\"Reference\"\s+\"([^\"]+)\"\s+\(at\s+([-\d.]+)\s+([-\d.]+)', sym_block)
    val_m = re.search(r'\(property\s+\"Value\"\s+\"([^\"]+)\"', sym_block)
    fp_m = re.search(r'\(property\s+\"Footprint\"\s+\"([^\"]+)\"', sym_block)
    if ref_m and val_m:
        print(f"Symbol {ref_m.group(1)}: {val_m.group(1)} at ({ref_m.group(2)}, {ref_m.group(3)}) fp={fp_m.group(1) if fp_m else 'None'}")
