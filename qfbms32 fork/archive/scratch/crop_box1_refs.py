from PIL import Image, ImageDraw
import os

pcb = r"c:\Users\quinn\Documents\GitHub\Fungineers PCB designs\qfbms32 ai pcb"
out = os.path.join(pcb, "scratch")

# Board ~130x32; CAD maps board to full image
bw, bh = 130.0, 32.0
cx, cy, w, h = 29.15, 5.70, 1.75, 0.95

for name in [
    "_reference/vfbms32_cad_top_reference_rotated.png",
    "_reference/vfbms32_real_top_hd.png",
    "qfbms32_3d_top.png",
]:
    path = os.path.join(pcb, name)
    if not os.path.exists(path):
        print("missing", name)
        continue
    im = Image.open(path).convert("RGBA")
    sx = im.width / bw
    sy = im.height / bh
    pad = 5.0  # mm
    x0 = int((cx - w / 2 - pad) * sx)
    y0 = int((cy - h / 2 - pad) * sy)
    x1 = int((cx + w / 2 + pad) * sx)
    y1 = int((cy + h / 2 + pad) * sy)
    x0, y0 = max(0, x0), max(0, y0)
    x1, y1 = min(im.width, x1), min(im.height, y1)
    crop = im.crop((x0, y0, x1, y1))
    draw = ImageDraw.Draw(crop)
    bx0 = int((cx - w / 2) * sx) - x0
    by0 = int((cy - h / 2) * sy) - y0
    bx1 = int((cx + w / 2) * sx) - x0
    by1 = int((cy + h / 2) * sy) - y0
    draw.rectangle([bx0, by0, bx1, by1], outline=(0, 160, 255, 255), width=2)
    for rx, ry, label in [
        (29.5, 8.95, "R_GS1"),
        (29.5, 7.6, "R_G1"),
        (29.18, 10.85, "D_GS1"),
        (29.15, 5.70, "BOX1"),
    ]:
        px = int(rx * sx) - x0
        py = int(ry * sy) - y0
        if 0 <= px < crop.width and 0 <= py < crop.height:
            draw.ellipse([px - 3, py - 3, px + 3, py + 3], outline=(255, 80, 80, 255), width=2)
            draw.text((px + 5, py - 6), label, fill=(255, 80, 80, 255))
    out_path = os.path.join(out, f"box1_crop_{os.path.splitext(os.path.basename(name))[0]}.png")
    crop = crop.resize((crop.width * 4, crop.height * 4), Image.Resampling.NEAREST)
    crop.save(out_path)
    print("saved", out_path, "from", im.size)
