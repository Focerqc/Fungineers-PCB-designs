with open("VFBMS32.kicad_pcb", "r", encoding="utf-8") as f:
    text = f.read()

pos = text.find('"BZ1"')
if pos != -1:
    start = text.rfind('(footprint', 0, pos)
    end = text.find('(footprint', pos)
    print(text[start:end])
