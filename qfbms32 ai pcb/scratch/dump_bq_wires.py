import re
from pathlib import Path

sch = Path("qfbms32 ai pcb/qfbms32.kicad_sch").read_text(encoding="utf-8")

# Extract BQ pin positions from lib_symbols only (first big BQ symbol)
start = sch.find('(symbol "Battery_Management:BQ7695202PFB"')
# find the unit drawing with pins - look for VC1 pin specifically inside lib
chunk = sch[start : start + 25000]
pins = re.findall(
    r'\(pin (\w+) line\s*\(at ([0-9.-]+) ([0-9.-]+) ([0-9.-]+)\)\s*\(length ([0-9.]+)\)'
    r'[\s\S]*?\(name "([^"]+)"[\s\S]*?\(number "([^"]+)"',
    chunk,
)
print("lib pins found", len(pins))
for et, x, y, r, ln, name, num in pins[:25]:
    print(f"  {num:>3} {name:10} @({x},{y}) rot={r} len={ln} {et}")

sx, sy = 149.86, 100.33
print("\nAbsolute left-side VC tips:")
for et, x, y, r, ln, name, num in pins:
    if name.startswith("VC") or name in ("VSS", "SRP", "SRN", "BAT", "TS1", "TS2", "TS3"):
        ax, ay = sx + float(x), sy + float(y)
        print(f"  {num} {name:6} abs=({ax:.2f},{ay:.2f})")

# Wires near x=129.54
print("\nWires starting near 129.5:")
for m in re.finditer(
    r'\(wire\s*\(pts \(xy ([0-9.-]+) ([0-9.-]+)\) \(xy ([0-9.-]+) ([0-9.-]+)\)\)[\s\S]*?\)\s*\(label "([^"]+)"',
    sch,
):
    x0, y0, x1, y1, lab = m.groups()
    if abs(float(x0) - 129.54) < 0.1 or abs(float(x1) - 129.54) < 0.1:
        print(f"  {lab:12} ({x0},{y0})->({x1},{y1})")
