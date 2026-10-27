import re

with open('c:/Users/quinn/Desktop/AI PCB CAD/Q VFBMS32 AI PCB/VFBMS32.kicad_pcb', 'r') as f:
    text = f.read()

for m in re.finditer(r'\(footprint "TOLL-8_AGM15T03LL"[\s\S]*?\(property "Reference" "([^"]+)"', text):
    print(m.group(0)[:200])
    print('---')
