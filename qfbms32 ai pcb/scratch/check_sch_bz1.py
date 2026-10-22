with open("VFBMS32.kicad_sch", "r", encoding="utf-8") as f:
    text = f.read()

pos = text.find('"BZ1"')
if pos != -1:
    start = text.rfind('(symbol', 0, pos)
    end = text.find('(symbol', pos)
    print(text[start:end if end != -1 else start+1000])
