from PIL import Image
import os

cad_img_path = r"c:\Users\quinn\Documents\GitHub\Fungineers PCB designs\Q VFBMS32 AI PCB\_reference\vfbms32_cad_top_reference_rotated.png"
cad_img = Image.open(cad_img_path)
print("CAD reference image size:", cad_img.size)

# The board bounding box in VFBMS32:
# Board outline: length ~ 130mm, width ~ 32mm.
# Let's inspect board outline from kicad_pcb:
with open(r"c:\Users\quinn\Documents\GitHub\Fungineers PCB designs\Q VFBMS32 AI PCB\VFBMS32.kicad_pcb", "r", encoding="utf-8") as f:
    text = f.read()

import re
lines = re.findall(r'\(gr_line\s+\(start\s+([0-9\.\-]+)\s+([0-9\.\-]+)\)\s+\(end\s+([0-9\.\-]+)\s+([0-9\.\-]+)\)\s+\(stroke[^)]+\)\s+\(layer\s+"Edge.Cuts"\)', text)
xs = []
ys = []
for x1, y1, x2, y2 in lines:
    xs.extend([float(x1), float(x2)])
    ys.extend([float(y1), float(y2)])

if xs and ys:
    min_x, max_x = min(xs), max(xs)
    min_y, max_y = min(ys), max(ys)
    print(f"Board bounds: X [{min_x}, {max_x}] (W={max_x - min_x}), Y [{min_y}, {max_y}] (H={max_y - min_y})")
