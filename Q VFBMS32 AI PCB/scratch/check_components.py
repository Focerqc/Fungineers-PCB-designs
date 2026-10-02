import re

with open('c:/Users/quinn/Desktop/AI PCB CAD/Q VFBMS32 AI PCB/VFBMS32.kicad_pcb', 'r') as f:
    text = f.read()

fps = []
for m in re.finditer(r'\(footprint\s+\"([^\"]+)\"[\s\S]*?\(property\s+\"Reference\"\s+\"([^\"]+)\"[\s\S]*?\(property\s+\"Value\"\s+\"([^\"]+)\"', text):
    fps.append((m.group(2), m.group(1), m.group(3)))

print(f"Total footprints: {len(fps)}")
for ref, name, val in sorted(fps):
    if any(k in ref for k in ['USB', 'ESP', 'U7', 'CHG', 'BAT', 'Q1', 'Q2', 'BQ']):
        print(f"{ref}: {name} ({val})")
