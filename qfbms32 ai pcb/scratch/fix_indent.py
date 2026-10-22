with open(r"c:\Users\quinn\Desktop\AI PCB CAD\Q VFBMS32 AI PCB\VFBMS32.kicad_sch", "r", encoding="utf-8") as f:
    text = f.read()

# Fix the 3-tab indentation on line 2326:
text = text.replace('\t\t\t(symbol "vfbms:AGM15T03LL"', '\t\t(symbol "vfbms:AGM15T03LL"')

with open(r"c:\Users\quinn\Desktop\AI PCB CAD\Q VFBMS32 AI PCB\VFBMS32.kicad_sch", "w", encoding="utf-8") as f:
    f.write(text)

print("Fixed indentation!")
