sch_path = r"c:\Users\quinn\Documents\GitHub\Fungineers PCB designs\qfbms32 ai pcb\qfbms32.kicad_sch"
with open(sch_path, "r", encoding="utf-8") as f:
    sch = f.read()

# Let's inspect all wires and labels near lines 3300..3600
lines = sch.splitlines()
for i in range(3250, min(len(lines), 3650)):
    print(f"{i+1:4d}: {lines[i]}")
