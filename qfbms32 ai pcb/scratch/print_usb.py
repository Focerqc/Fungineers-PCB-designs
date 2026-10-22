import re

pcb_path = r"c:\Users\quinn\Documents\GitHub\Fungineers PCB designs\Q VFBMS32 AI PCB\VFBMS32.kicad_pcb"
with open(pcb_path, "r", encoding="utf-8") as f:
    txt = f.read()

m = re.search(r'\(footprint [^\n]*\n[\s\S]*?\"Reference\" \"J_USB1\"[\s\S]*?\n\t\)', txt)
if m:
    print(m.group(0))
else:
    print("Not found")
