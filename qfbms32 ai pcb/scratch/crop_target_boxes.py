import os
from PIL import Image

pcb_dir = r"c:\Users\quinn\Documents\GitHub\Fungineers PCB designs\qfbms32 ai pcb"
cad_img_path = os.path.join(pcb_dir, "_reference", "vfbms32_cad_top_reference_rotated.png")
real_img_path = os.path.join(pcb_dir, "_reference", "vfbms32_real_top_hd.png")
top_3d_path = os.path.join(pcb_dir, "qfbms32_3d_top.png")

cad_im = Image.open(cad_img_path)
real_im = Image.open(real_img_path)
top_3d_im = Image.open(top_3d_path)

print(f"CAD size: {cad_im.size}")
print(f"Real size: {real_im.size}")
print(f"3D size: {top_3d_im.size}")

# Board dimensions: 130mm x 32mm
# In CAD and 3D top, let's crop around X in [26..33]mm, Y in [2..20]mm
# Also crop each box individually
boxes = [
    {"name": "c1_box1", "label": "Color 1 Item 1 (X10)", "x": 29.75, "y": 17.20, "w": 1.6, "h": 0.8},
    {"name": "c1_box2", "label": "Color 1 Item 2 (X10)", "x": 29.50, "y": 7.60, "w": 1.6, "h": 0.8},
    {"name": "c1_box3", "label": "Color 1 Item 3 (X10)", "x": 29.20, "y": 4.05, "w": 1.6, "h": 0.8},
    {"name": "c2_box1", "label": "Color 2 Item 1 (474)", "x": 29.50, "y": 8.95, "w": 1.6, "h": 0.8},
]

# Overall region crop (X: 25..35, Y: 1..22)
def crop_box(im, x_mm, y_mm, span_x_mm=3.0, span_y_mm=3.0):
    w, h = im.size
    cx = int((x_mm / 130.0) * w)
    cy = int((y_mm / 32.0) * h)
    rx = int((span_x_mm / 130.0) * w)
    ry = int((span_y_mm / 32.0) * h)
    return im.crop((max(0, cx - rx), max(0, cy - ry), min(w, cx + rx), min(h, cy + ry)))

# Save overall region
crop_cad_region = crop_box(cad_im, 29.5, 11.0, span_x_mm=6.0, span_y_mm=11.0)
crop_cad_region.save(os.path.join(pcb_dir, "scratch", "cad_region_x29.png"))

crop_real_region = crop_box(real_im, 29.5, 11.0, span_x_mm=6.0, span_y_mm=11.0)
crop_real_region.save(os.path.join(pcb_dir, "scratch", "real_region_x29.png"))

crop_3d_region = crop_box(top_3d_im, 29.5, 11.0, span_x_mm=6.0, span_y_mm=11.0)
crop_3d_region.save(os.path.join(pcb_dir, "scratch", "3d_region_x29.png"))

for b in boxes:
    c_cad = crop_box(cad_im, b["x"], b["y"], 1.5, 1.2)
    c_cad.save(os.path.join(pcb_dir, "scratch", f"{b['name']}_cad.png"))
    c_real = crop_box(real_im, b["x"], b["y"], 1.5, 1.2)
    c_real.save(os.path.join(pcb_dir, "scratch", f"{b['name']}_real.png"))

print("Cropped regions successfully!")
