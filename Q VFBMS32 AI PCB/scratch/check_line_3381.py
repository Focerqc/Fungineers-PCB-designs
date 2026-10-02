with open(r"c:\Users\quinn\Desktop\AI PCB CAD\Q VFBMS32 AI PCB\VFBMS32.kicad_sch", "r", encoding="utf-8") as f:
    lines = f.readlines()

print(f"Total lines: {len(lines)}")
for i in range(max(0, 3370), min(len(lines), 3395)):
    print(f"{i+1:4}: {lines[i]}", end="")
