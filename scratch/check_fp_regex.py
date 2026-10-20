import re

pcb_path = r"c:\Users\quinn\Documents\GitHub\Fungineers PCB designs\Q VFBMS32 AI PCB\VFBMS32.kicad_pcb"
with open(pcb_path, "r", encoding="utf-8") as f:
    pcb = f.read()

# Let's find D_V1, D_V2, D_V3 blocks
for ref in ['D_V1', 'D_V2', 'D_V3']:
    m = re.search(r'\t\(footprint[^\n]*\n(?:[^\n]*\n)*?\t\t\(property "Reference" "' + ref + r'"[\s\S]*?\n\t\)', pcb)
    if m:
        print(f"Found {ref} footprint block (len={len(m.group(0))})")
    else:
        print(f"Not found: {ref}")
