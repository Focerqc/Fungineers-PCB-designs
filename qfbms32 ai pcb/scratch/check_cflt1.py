with open('VFBMS32.kicad_pcb', 'r', encoding='utf-8') as f:
    text = f.read()

pos = text.find('"C_FLT1"')
start = text.rfind('(footprint', 0, pos)
end = text.find('(footprint', pos)
print(text[start:end])
