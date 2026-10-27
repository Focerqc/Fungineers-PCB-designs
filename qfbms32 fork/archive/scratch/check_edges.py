import re

pcb_path = r"c:\Users\quinn\Documents\GitHub\Fungineers PCB designs\Q VFBMS32 AI PCB\VFBMS32.kicad_pcb"
with open(pcb_path, "r", encoding="utf-8") as f:
    text = f.read()

edges = re.findall(r'\(gr_line[\s\S]*?\"Edge\.Cuts\"[\s\S]*?\)', text)
for e in edges:
    print(e)
