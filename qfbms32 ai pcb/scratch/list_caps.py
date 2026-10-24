import re

with open('qfbms32.kicad_pcb', 'r', encoding='utf-8') as f:
    pcb = f.read()

c_fps = re.findall(r'\(property "Reference" "(C[^"]+)"', pcb)
print('Capacitors on PCB:', sorted(set(c_fps)))
