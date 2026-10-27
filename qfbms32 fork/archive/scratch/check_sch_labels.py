with open("VFBMS32.kicad_sch", "r", encoding="utf-8") as f:
    text = f.read()

import re
labels = re.findall(r'\(label\s+"([^"]+)".*?\(at\s+([0-9\.\-]+)\s+([0-9\.\-]+)', text)
for l in labels:
    print(f"Label: {l[0]} at ({l[1]}, {l[2]})")
