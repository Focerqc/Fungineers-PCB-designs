with open("VFBMS32.kicad_sch", "r", encoding="utf-8") as f:
    text = f.read()

import re
chunks = text.split('(symbol')
for c in chunks:
    if any(r in c for r in ['D_CHG1', 'R_CHG1']):
        print("=== SYMBOL CHUNK ===")
        print(c[:1500])
