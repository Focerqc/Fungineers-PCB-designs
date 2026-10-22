import re

with open(r'c:\Users\quinn\Desktop\AI PCB CAD\Q VFBMS32 AI PCB\vfbms.pretty\USB_C_Receptacle_16P.kicad_mod', 'r') as f:
    text = f.read()

print("USB_C pads sample:")
for m in re.finditer(r'\(pad\s+\"([^\"]+)\"[\s\S]*?\(at\s+([\d.-]+)\s+([\d.-]+)\)', text):
    print(f"Pad {m.group(1)}: at ({m.group(2)}, {m.group(3)})")

models = re.findall(r'\(model\s+[\s\S]*?\n\t\)', text)
print("Model block:", models)
