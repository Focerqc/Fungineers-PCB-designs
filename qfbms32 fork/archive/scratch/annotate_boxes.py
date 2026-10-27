from PIL import Image, ImageDraw

cad = Image.open(r"c:\Users\quinn\Documents\GitHub\Fungineers PCB designs\Q VFBMS32 AI PCB\_reference\vfbms32_cad_top_reference_rotated.png").convert("RGBA")
sx = cad.width / 130.0
sy = cad.height / 32.0

# Region X: 82 to 95 mm, Y: 0 to 10 mm
x1_full = int(82 * sx)
y1_full = int(0 * sy)
x2_full = int(95 * sx)
y2_full = int(10 * sy)

overlay = cad.copy()
draw = ImageDraw.Draw(overlay)

boxes = [
    (1, 90.05, 1.10, 1.00, 1.60),
    (2, 90.08, 4.53, 0.85, 1.55),
    (3, 86.55, 4.47, 0.80, 1.45),
]

for num, bx, by, bw, bh in boxes:
    # bounding box
    rx1 = int((bx - bw/2) * sx)
    ry1 = int((by - bh/2) * sy)
    rx2 = int((bx + bw/2) * sx)
    ry2 = int((by + bh/2) * sy)
    draw.rectangle([rx1, ry1, rx2, ry2], outline=(0, 255, 255, 255), width=1)
    draw.text((rx1, ry1 - 8), str(num), fill=(255, 0, 0, 255))

crop_ctx = overlay.crop((x1_full, y1_full, x2_full, y2_full))
# scale up 4x for easy viewing
crop_ctx = crop_ctx.resize((crop_ctx.width * 4, crop_ctx.height * 4), Image.Resampling.NEAREST)
crop_ctx.save(r"c:\Users\quinn\Documents\GitHub\Fungineers PCB designs\Q VFBMS32 AI PCB\scratch\boxes_annotated_cad.png")

# Also do the same on real photo
real = Image.open(r"c:\Users\quinn\Documents\GitHub\Fungineers PCB designs\Q VFBMS32 AI PCB\_reference\vfbms32_real_top_hd.png").convert("RGBA")
sx_r = real.width / 130.0
sy_r = real.height / 32.0
overlay_r = real.copy()
draw_r = ImageDraw.Draw(overlay_r)
for num, bx, by, bw, bh in boxes:
    rx1 = int((bx - bw/2) * sx_r)
    ry1 = int((by - bh/2) * sy_r)
    rx2 = int((bx + bw/2) * sx_r)
    ry2 = int((by + bh/2) * sy_r)
    draw_r.rectangle([rx1, ry1, rx2, ry2], outline=(0, 255, 255, 255), width=2)
    draw_r.text((rx1, ry1 - 10), str(num), fill=(255, 0, 0, 255))

crop_r = overlay_r.crop((int(82 * sx_r), int(0 * sy_r), int(95 * sx_r), int(10 * sy_r)))
crop_r = crop_r.resize((crop_r.width * 2, crop_r.height * 2), Image.Resampling.NEAREST)
crop_r.save(r"c:\Users\quinn\Documents\GitHub\Fungineers PCB designs\Q VFBMS32 AI PCB\scratch\boxes_annotated_real.png")

print("Saved annotated crops")
