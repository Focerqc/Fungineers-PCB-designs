with open(r"c:\Users\quinn\Desktop\AI PCB CAD\Q VFBMS32 AI PCB\VFBMS32.kicad_sch", "r", encoding="utf-8") as f:
    text = f.read()

# Replace any \t\t(symbol (lib_id "vfbms: or \t\t(symbol (lib_id "Device:
text = text.replace('\t\t(symbol (lib_id "vfbms:', '\t(symbol (lib_id "vfbms:')
text = text.replace('\t\t(symbol (lib_id "Device:', '\t(symbol (lib_id "Device:')

with open(r"c:\Users\quinn\Desktop\AI PCB CAD\Q VFBMS32 AI PCB\VFBMS32.kicad_sch", "w", encoding="utf-8") as f:
    f.write(text)

print("Adjusted symbol indentation!")
