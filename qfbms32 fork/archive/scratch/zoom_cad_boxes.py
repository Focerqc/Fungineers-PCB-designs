import os
from PIL import Image

pcb_dir = r"c:\Users\quinn\Documents\GitHub\Fungineers PCB designs\qfbms32 ai pcb"
brain_dir = r"C:\Users\quinn\.gemini\antigravity-ide\brain\7bc5fde5-e6cf-413a-9764-f83c0e8df3ae"

cad = Image.open(os.path.join(pcb_dir, "_reference", "vfbms32_cad_top_reference_rotated.png"))
cw, ch = cad.size

boxes = [
    {"name": "cad_c1_b1_y17_2", "x": 29.75, "y": 17.20, "w": 1.6, "h": 0.8},
    {"name": "cad_c1_b2_y7_6",  "x": 29.50, "y": 7.60,  "w": 1.6, "h": 0.8},
    {"name": "cad_c1_b3_y4_05", "x": 29.20, "y": 4.05,  "w": 1.6, "h": 0.8},
    {"name": "cad_c2_b1_y8_95", "x": 29.50, "y": 8.95,  "w": 1.6, "h": 0.8},
]

for b in boxes:
    # box center
    cx = (b["x"] / 130.0) * cw
    cy = (b["y"] / 32.0) * ch
    # crop 3mm around center
    rx = (3.0 / 130.0) * cw
    ry = (3.0 / 32.0) * ch
    crop = cad.crop((cx - rx, cy - ry, cx + rx, cy + ry))
    # resize 5x for easy visual inspection
    crop_5x = crop.resize((crop.width * 5, crop.height * 5), Image.Resampling.NEAREST)
    crop_5x.save(os.path.join(brain_dir, f"{b['name']}_zoom.png"))
    print(f"Saved {b['name']}_zoom.png")
