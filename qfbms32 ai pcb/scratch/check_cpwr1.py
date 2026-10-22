with open('VFBMS32.kicad_pcb', 'r', encoding='utf-8') as f:
    pcb = f.read()

pos = pcb.find('"C_PWR1"')
start = pcb.rfind('(footprint', 0, pos)
end = pcb.find('(footprint', pos)
print(pcb[start:end])
