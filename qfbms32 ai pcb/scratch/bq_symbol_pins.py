import re
from pathlib import Path

t = Path(r"qfbms32 ai pcb/qfbms32.kicad_sch").read_text(encoding="utf-8")
i = t.find('(symbol "Battery_Management:BQ7695202PFB"')
j = t.find('\n\t\t(symbol "', i + 10)
blk = t[i:j]
pins = re.findall(
    r'\(pin [^\n]+\n(?:.*\n)*?\s+\(name "([^"]+)"[\s\S]*?\(number "([^"]+)"',
    blk,
)
print("count", len(pins))
rows = []
for name, num in pins:
    rows.append((int(num) if num.isdigit() else 999, num, name))
for _, num, name in sorted(rows):
    print(f"{num:>4}  {name}")
