import re

with open('qfbms32.kicad_sch', 'r', encoding='utf-8') as f:
    text = f.read()

# find wires and labels near (175, 105)
for line in text.splitlines():
    if any(k in line for k in ["175.0", "195.0", "205.0", "215.0", "CHG_EN", "PCHG", "DCHG"]):
        print(line)
