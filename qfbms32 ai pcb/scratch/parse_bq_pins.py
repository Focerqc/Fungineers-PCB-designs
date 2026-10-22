import re

sch_path = r"c:\Users\quinn\Desktop\AI PCB CAD\Q VFBMS32 AI PCB\VFBMS32.kicad_sch"
with open(sch_path, "r", encoding="utf-8") as f:
    text = f.read()

# Find symbol BQ7695202PFB pins
pins = re.findall(r'\(pin\s+\w+\s+\w+\s+\(at\s+([-\d.]+)\s+([-\d.]+)\s+([-\d.]+)\)\s+\(length\s+[-\d.]+\)\s+\(name\s+\"([^\"]+)\"[\s\S]*?\(number\s+\"([^\"]+)\"', text)

print(f"Total BQ76952 pins: {len(pins)}")
for x, y, rot, name, num in sorted(pins, key=lambda p: int(p[4]) if p[4].isdigit() else 999):
    print(f"  Pin {num:2}: {name:12} at ({x}, {y}, rot={rot})")
