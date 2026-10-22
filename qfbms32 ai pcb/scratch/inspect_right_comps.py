import re

with open('VFBMS32.kicad_pcb', 'r', encoding='utf-8') as f:
    text = f.read()

# Let's parse all footprints with their reference, position, rotation
fps = []
for m in re.finditer(r'\(footprint\s+"([^"]+)"([\s\S]*?\n\t\))', text):
    fp_name = m.group(1)
    body = m.group(2)
    ref = re.search(r'\(property "Reference" "([^"]+)"', body)
    val = re.search(r'\(property "Value" "([^"]+)"', body)
    at = re.search(r'\(at\s+([0-9\.\-]+)\s+([0-9\.\-]+)(?:\s+([0-9\.\-]+))?\)', body)
    if ref and at:
        fps.append({
            'ref': ref.group(1),
            'val': val.group(1) if val else '',
            'x': float(at.group(1)),
            'y': float(at.group(2)),
            'rot': float(at.group(3)) if at.group(3) else 0.0,
            'fp': fp_name
        })

print("=== ALL COMPONENTS ON RIGHT SIDE (X > 90mm) ===")
fps_right = [f for f in fps if f['x'] > 90]
fps_right.sort(key=lambda item: (item['x'], item['y']))
for f in fps_right:
    print(f"{f['ref']:<12} : {f['val']:<20} at ({f['x']:6.2f}, {f['y']:6.2f}, rot={f['rot']:5.1f}) | {f['fp']}")
