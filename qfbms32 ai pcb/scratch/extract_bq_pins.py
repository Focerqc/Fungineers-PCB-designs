import re
from pathlib import Path

sch = Path("qfbms32 ai pcb/qfbms32.kicad_sch").read_text(encoding="utf-8")
# Grab BQ7695202PFB_1_1 unit body
start = sch.find('(symbol "BQ7695202PFB_1_1"')
end = sch.find('(symbol "BQ7695202PFB_', start + 10)
body = sch[start:end]
# Each pin block has name and number
blocks = re.findall(r"\(pin\b.*?\)\n\t\t\t\)", body, re.S)
mapping = {}
for blk in blocks:
    nm = re.search(r'\(name "([^"]+)"', blk)
    nu = re.search(r'\(number "([^"]+)"', blk)
    if nm and nu:
        mapping[nu.group(1)] = nm.group(1)
for num in sorted(mapping, key=lambda x: int(x) if x.isdigit() else 999):
    print(f"{num:4} {mapping[num]}")
print("total", len(mapping))
