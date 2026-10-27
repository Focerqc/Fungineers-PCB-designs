with open("qfbms32 ai pcb/qfbms32.kicad_sch", "r", encoding="utf-8", errors="ignore") as f:
    text = f.read()

import re
refs = re.findall(r'\(property\s+"Reference"\s+"([^"]+)"', text)
print(f"All references in schematic ({len(refs)}):", sorted(list(set(refs))))
