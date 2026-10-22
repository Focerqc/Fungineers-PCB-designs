import re

with open("VFBMS32.kicad_pcb", "r", encoding="utf-8") as f:
    text = f.read()

footprints = text.split("(footprint ")
print(f"Total footprints: {len(footprints)-1}")

for chunk in footprints[1:]:
    ref_m = re.search(r'\(property\s+"Reference"\s+"([^"]+)"', chunk)
    val_m = re.search(r'\(property\s+"Value"\s+"([^"]+)"', chunk)
    at_m = re.search(r'\(at\s+([0-9\.\-]+)\s+([0-9\.\-]+)(?:\s+([0-9\.\-]+))?\)', chunk)
    fp_m = re.match(r'"([^"]+)"', chunk)
    
    ref = ref_m.group(1) if ref_m else "?"
    val = val_m.group(1) if val_m else "?"
    fp = fp_m.group(1) if fp_m else "?"
    
    if at_m:
        x, y = float(at_m.group(1)), float(at_m.group(2))
        rot = float(at_m.group(3)) if at_m.group(3) else 0.0
    else:
        x, y, rot = 0, 0, 0
        
    model_m = re.search(r'\(model\s+"([^"]+)"\s+\(offset\s+\(xyz\s+([^\)]+)\)\)', chunk)
    offset = model_m.group(2) if model_m else "N/A"
    model_path = model_m.group(1) if model_m else "None"
    
    if x < 20 and y < 25:
        print(f"Ref: {ref:10} Val: {val:12} FP: {fp:20} Pos: ({x:5.2f}, {y:5.2f}, rot={rot:5.1f}) Offset: {offset} Model: {model_path}")
