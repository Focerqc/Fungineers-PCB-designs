import json
import os
from PIL import Image, ImageDraw, ImageFont

brain_dir = r"C:\Users\quinn\.gemini\antigravity-ide\brain\7bc5fde5-e6cf-413a-9764-f83c0e8df3ae"
os.makedirs(brain_dir, exist_ok=True)

pcb_dir = r"c:\Users\quinn\Documents\GitHub\Fungineers PCB designs\qfbms32 ai pcb"

# Load boxes
boxes_path = os.path.join(pcb_dir, "qfbms32.boxes.json")
with open(boxes_path, "r") as f:
    boxes_data = json.load(f)

# Colors
color_map = {}
for c in boxes_data["colors"]:
    color_map[c["id"]] = c

boxes = boxes_data["boxes"]
print("Boxes:")
for b in boxes:
    cinfo = color_map.get(b["c"], {})
    print(f"ID={b['id']} Color={cinfo.get('hex')} Note={cinfo.get('note')} Pos=({b['x']:.2f}, {b['y']:.2f}) Size=({b['w']:.2f}x{b['h']:.2f})")

# Let's inspect vfbms32_cad_top_reference_rotated.png
cad_path = os.path.join(pcb_dir, "_reference", "vfbms32_cad_top_reference_rotated.png")
cad_im = Image.open(cad_path).convert("RGBA")
cw, ch = cad_im.size

# In CAD reference, board is 130mm x 32mm
# Let's draw the boxes on a copy of CAD reference
cad_annotated = cad_im.copy()
draw = ImageDraw.Draw(cad_annotated)
font = ImageFont.load_default()

for b in boxes:
    cinfo = color_map.get(b["c"], {})
    hex_col = cinfo.get("hex", "#ffffff")
    # convert hex to RGBA
    h = hex_col.lstrip("#")
    rgb = tuple(int(h[i:i+2], 16) for i in (0, 2, 4))
    
    # KiCad mm to pixels
    bx = (b["x"] / 130.0) * cw
    by = (b["y"] / 32.0) * ch
    bw = (b["w"] / 130.0) * cw
    bh = (b["h"] / 32.0) * ch
    
    x0, y0 = bx - bw/2, by - bh/2
    x1, y1 = bx + bw/2, by + bh/2
    draw.rectangle([x0, y0, x1, y1], outline=rgb, width=2)
    draw.text((x0, y0 - 10), cinfo.get("note", "")[:15], fill=rgb, font=font)

# Crop the region around X=24..35mm, Y=2..20mm
crop_x0 = int((23.0 / 130.0) * cw)
crop_x1 = int((35.0 / 130.0) * cw)
crop_y0 = int((1.0 / 32.0) * ch)
crop_y1 = int((21.0 / 32.0) * ch)

crop_cad = cad_annotated.crop((crop_x0, crop_y0, crop_x1, crop_y1))
out_cad = os.path.join(brain_dir, "cad_boxes_crop.png")
crop_cad.save(out_cad)
print(f"Saved CAD annotated crop to {out_cad}")

# Also crop unannotated CAD for pristine view
crop_cad_raw = cad_im.crop((crop_x0, crop_y0, crop_x1, crop_y1))
crop_cad_raw.save(os.path.join(brain_dir, "cad_raw_crop.png"))

# Let's inspect real_top_hd
real_path = os.path.join(pcb_dir, "_reference", "vfbms32_real_top_hd.png")
if os.path.exists(real_path):
    real_im = Image.open(real_path).convert("RGBA")
    rw, rh = real_im.size
    # In real_top_hd, let's see how it aligns
    rx0 = int((23.0 / 130.0) * rw)
    rx1 = int((35.0 / 130.0) * rw)
    ry0 = int((1.0 / 32.0) * rh)
    ry1 = int((21.0 / 32.0) * rh)
    crop_real = real_im.crop((rx0, ry0, rx1, ry1))
    crop_real.save(os.path.join(brain_dir, "real_top_hd_crop.png"))
    print("Saved real_top_hd_crop.png")
