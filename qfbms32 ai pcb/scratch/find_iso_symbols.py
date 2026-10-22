import os, re

sym_dir = r'C:\Program Files\KiCad\10.0\share\kicad\symbols'
for f in os.listdir(sym_dir):
    if f.endswith('.kicad_sym'):
        p = os.path.join(sym_dir, f)
        with open(p, 'r', encoding='utf-8', errors='ignore') as sf:
            s = sf.read()
            if 'ISO1050' in s:
                print(f"Found in {f}")
                for m in re.finditer(r'\(symbol\s+"([^"]*ISO1050[^"]*)"', s):
                    print(f"  Symbol name: {m.group(1)}")
