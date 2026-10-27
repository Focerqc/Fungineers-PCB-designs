import re

with open(r'c:\Users\quinn\Desktop\AI PCB CAD\Q VFBMS32 AI PCB\vfbms.pretty\ESP32-C3-MINI-1.kicad_mod', 'r') as f:
    text = f.read()

models = re.findall(r'\(model\s+[\s\S]*?\n\t\)', text)
print("ESP Model block:", models)

# Find bounding box / pads in ESP32 footprint
pads = []
for m in re.finditer(r'\(pad\s+\"([^\"]+)\"[\s\S]*?\(at\s+([\d.-]+)\s+([\d.-]+)\)', text):
    pads.append((m.group(1), float(m.group(2)), float(m.group(3))))

print(f"Total pads: {len(pads)}")
xs = [p[1] for p in pads]
ys = [p[2] for p in pads]
print(f"Pads X range: {min(xs)} to {max(xs)}")
print(f"Pads Y range: {min(ys)} to {max(ys)}")
