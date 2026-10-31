import re
from pathlib import Path

sch = Path("qfbms32 ai pcb/qfbms32.kicad_sch").read_text(encoding="utf-8")
start = sch.find('(symbol "BQ7695202PFB_1_1"')
# end at next sibling symbol at same indent under lib
end = sch.find('\n\t\t(symbol "', start + 10)
body = sch[start:end]
pins = []
for m in re.finditer(
    r'\(pin\b[^)]*\n(?:.*\n)*?\s*\(name "([^"]+)"(?:.*\n)*?\s*\(number "([^"]+)"',
    body,
):
    pins.append((m.group(2), m.group(1)))
# fallback simpler line-oriented
if len(pins) < 40:
    pins = []
    chunks = re.split(r"\n\t\t\t\t\(pin ", body)
    for ch in chunks[1:]:
        nm = re.search(r'\(name "([^"]+)"', ch)
        nu = re.search(r'\(number "([^"]+)"', ch)
        if nm and nu:
            pins.append((nu.group(1), nm.group(1)))
for num, name in sorted(pins, key=lambda x: int(x[0]) if x[0].isdigit() else 999):
    print(f"{num:4} {name}")
print("total", len(pins))
