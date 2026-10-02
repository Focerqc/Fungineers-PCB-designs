with open(r"c:\Users\quinn\Desktop\AI PCB CAD\Q VFBMS32 AI PCB\VFBMS32.kicad_sch", "r", encoding="utf-8") as f:
    lines = f.readlines()

for i in range(2315, 2335):
    print(f"{i+1:4}: {repr(lines[i])}")
