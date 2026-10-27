import os
from PIL import Image, ImageDraw, ImageFont

brain_dir = r"C:\Users\quinn\.gemini\antigravity-ide\brain\7bc5fde5-e6cf-413a-9764-f83c0e8df3ae"
pcb_dir = r"c:\Users\quinn\Documents\GitHub\Fungineers PCB designs\qfbms32 ai pcb"

# 1. 3D top render
im_3d = Image.open(os.path.join(pcb_dir, "qfbms32_3d_top.png"))
w_3d, h_3d = im_3d.size

# Board is 130mm x 32mm
# We want X: 24..34mm, Y: 1..21mm
x0_3d = int((24.0 / 130.0) * w_3d)
x1_3d = int((34.0 / 130.0) * w_3d)
y0_3d = int((1.0 / 32.0) * h_3d)
y1_3d = int((21.0 / 32.0) * h_3d)
crop_3d = im_3d.crop((x0_3d, y0_3d, x1_3d, y1_3d))
crop_3d.save(os.path.join(brain_dir, "crop_3d_new_col.png"))

# 2. CAD reference annotated
im_cad = Image.open(os.path.join(brain_dir, "cad_boxes_crop.png"))

# 3. Real HD top
im_real = Image.open(os.path.join(brain_dir, "real_top_hd_crop.png"))

# Let's normalize heights to 700px
target_h = 700
def resize_to_h(img, target_h):
    aspect = target_h / img.height
    return img.resize((int(img.width * aspect), target_h), Image.Resampling.LANCZOS)

cad_res = resize_to_h(im_cad, target_h)
new_res = resize_to_h(crop_3d, target_h)
real_res = resize_to_h(im_real, target_h)

pad = 12
banner_h = 45
total_w = cad_res.width + new_res.width + real_res.width + pad * 4
canvas_h = target_h + banner_h + pad * 2

canvas = Image.new("RGB", (total_w, canvas_h), (24, 28, 36))
draw = ImageDraw.Draw(canvas)

font = ImageFont.load_default()

# Panel 1: CAD Reference with Boxes
x = pad
canvas.paste(cad_res, (x, banner_h + pad))
draw.text((x + 10, 15), "1. CAD REFERENCE (USER BOXES)", fill=(78, 161, 255), font=font)

# Panel 2: New KiCad 3D Placement
x += cad_res.width + pad
canvas.paste(new_res, (x, banner_h + pad))
draw.text((x + 10, 15), "2. NEW KICAD 3D PLACEMENT", fill=(80, 250, 120), font=font)

# Panel 3: Physical PCB
x += new_res.width + pad
canvas.paste(real_res, (x, banner_h + pad))
draw.text((x + 10, 15), "3. PHYSICAL BOARD (VFBMS32)", fill=(255, 180, 80), font=font)

out_comp = os.path.join(brain_dir, "col1_col2_comparison.png")
canvas.save(out_comp)
print(f"Saved 3-way visual comparison to {out_comp}")
