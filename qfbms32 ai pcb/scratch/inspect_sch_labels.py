with open('VFBMS32.kicad_sch', 'r', encoding='utf-8') as f:
    text = f.read()

import re
print("Labels and their coordinates in VFBMS32.kicad_sch:")
for m in re.finditer(r'\((label|global_label|hierarchical_label)\s+"([^"]+)"[\s\S]*?\(at\s+([0-9\.\-]+)\s+([0-9\.\-]+)', text):
    print(f"  {m.group(1):<15} : {m.group(2):<20} at ({m.group(3)}, {m.group(4)})")
