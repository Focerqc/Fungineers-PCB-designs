import re

with open(r'c:\Users\quinn\Desktop\AI PCB CAD\Q VFBMS32 AI PCB\VFBMS32.kicad_pcb', 'r', encoding='utf-8') as f:
    text = f.read()

for ref in ['U_ESP1', 'J_USB1']:
    m = re.search(r'(\(footprint\s+\"[^\"]+\"[\s\S]*?\(property\s+\"Reference\"\s+\"' + ref + r'\"[\s\S]*?\n\t\))', text)
    if m:
        print(f"=== {ref} ===")
        print(m.group(1)[:400])
        print("...")
        models = re.findall(r'\(model\s+[\s\S]*?\n\t\t\)', m.group(1))
        print("Models:", models)
