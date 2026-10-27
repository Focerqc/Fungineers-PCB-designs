sch_path = r"c:\Users\quinn\Documents\GitHub\Fungineers PCB designs\qfbms32 ai pcb\qfbms32.kicad_sch"
with open(sch_path, "r", encoding="utf-8") as f:
    text = f.read()

import re
matches = re.findall(r'\(symbol\s+\(lib_id\s+"([^"]+)".*?\(property\s+"Reference"\s+"([^"]+)".*?\(property\s+"Value"\s+"([^"]+)".*?\(property\s+"Footprint"\s+"([^"]+)"', text, re.DOTALL)
print(f"Total symbols matched: {len(matches)}")
for lib, ref, val, fp in matches:
    if any(k in ref for k in ["Q", "SSR", "R_G", "R_CHG", "R_DSG", "D_CHG", "C_FLT", "D_SEC", "C_DISC"]):
        print(f"{ref:12s} {val:20s} {fp:35s} {lib}")
