import re

with open('c:/Users/quinn/Desktop/AI PCB CAD/Q VFBMS32 AI PCB/VFBMS32.kicad_pcb', 'r') as f:
    text = f.read()

footprints = re.findall(r'\(footprint\s+\"([^\"]+)\"[\s\S]*?\(property\s+\"Reference\"\s+\"([^\"]+)\"[\s\S]*?\n\t\)', text)

for m in re.finditer(r'\(footprint\s+\"([^\"]+)\"([\s\S]*?\(property\s+\"Reference\"\s+\"([^\"]+)\"[\s\S]*?)\n\t\)', text):
    fp_name = m.group(1)
    block = m.group(2)
    ref = m.group(3)
    models = re.findall(r'\(model\s+\"([^\"]+)\"', block)
    if ref in ['J_USB1', 'U_ESP1', 'Q1', 'Q2', 'J_CHG1', 'J_BAT1', 'U7']:
        print(f"Ref: {ref}, Footprint: {fp_name}")
        print(f"  Models: {models}")
