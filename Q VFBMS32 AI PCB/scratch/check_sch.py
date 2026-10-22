import re

with open('VFBMS32.kicad_sch', 'r', encoding='utf-8') as f:
    sch = f.read()

# Let's find all instances of symbol definitions
pattern = r'(\(symbol\s+\(lib_id\s+"[^"]+"\)\s+\(at\s+[0-9\.\-\s]+\).*?\(property\s+"Reference"\s+"([^"]+)".*?\n\t\))'
symbols = re.findall(pattern, sch, re.DOTALL)
print(f"Total symbols matched: {len(symbols)}")
for full, ref in symbols:
    if ref in ['D_CHG1', 'D_CHG2', 'D_CHG3', 'R_CHG1', 'Q1', 'Q2', 'J_CHG1', 'J_BAT1']:
        print(f"--- Symbol: {ref} ---")
        print(full[:600])

# Let's check labels / wires around power stage
labels = re.findall(r'\(label\s+"([^"]+)"\s+\(at\s+([0-9\.\-]+)\s+([0-9\.\-]+)', sch)
print(f"Labels found ({len(labels)}): {labels[:20]}")
global_labels = re.findall(r'\(global_label\s+"([^"]+)"\s+\(at\s+([0-9\.\-]+)\s+([0-9\.\-]+)', sch)
print(f"Global labels found ({len(global_labels)}): {global_labels[:20]}")
