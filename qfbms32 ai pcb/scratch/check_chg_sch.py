import re

with open('qfbms32.kicad_sch', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if "D_CHG1" in l or "R_CHG1" in l:
        print("".join(lines[max(0, i-10):min(len(lines), i+30)]))
        print("="*40)
