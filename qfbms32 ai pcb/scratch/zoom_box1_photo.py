"""Zoom the user-provided Box1 photo for identification."""
from PIL import Image, ImageDraw, ImageEnhance
import os

src = r"C:\Users\quinn\.cursor\projects\c-Users-quinn-Documents-GitHub-Fungineers-PCB-designs\assets\c__Users_quinn_AppData_Roaming_Cursor_User_workspaceStorage_967e551abd6422f9523b2b7b309cd895_images_image-a2724e5b-7165-4c7c-9662-db4fa008ce2f.jpg"
out_dir = r"c:\Users\quinn\Documents\GitHub\Fungineers PCB designs\qfbms32 ai pcb\scratch"
im = Image.open(src).convert("RGB")
print("photo size", im.size)

# Blue box is roughly center-upper; estimate from typical annotation
# Scan for blue-ish pixels to find the box
pixels = im.load()
w, h = im.size
blues = []
for y in range(0, h, 2):
    for x in range(0, w, 2):
        r, g, b = pixels[x, y]
        if b > 150 and b > r + 40 and b > g + 20 and r < 120:
            blues.append((x, y))
if blues:
    xs = [p[0] for p in blues]
    ys = [p[1] for p in blues]
    x0, x1 = min(xs), max(xs)
    y0, y1 = min(ys), max(ys)
    print("blue bbox", x0, y0, x1, y1)
    # expand around component
    pad = 80
    crop = im.crop(
        (max(0, x0 - pad), max(0, y0 - pad), min(w, x1 + pad), min(h, y1 + pad))
    )
else:
    # fallback center crop
    crop = im.crop((w // 4, h // 6, 3 * w // 4, 2 * h // 3))

crop = crop.resize((crop.width * 3, crop.height * 3), Image.Resampling.NEAREST)
# slight contrast boost
crop = ImageEnhance.Contrast(crop).enhance(1.3)
crop = ImageEnhance.Sharpness(crop).enhance(1.5)
out = os.path.join(out_dir, "box1_user_photo_zoom.png")
crop.save(out)
print("saved", out)

# Also make a tight crop of just the component interior of blue box
if blues:
    # inset from blue border
    inset = 8
    tight = im.crop((x0 + inset, y0 + inset, x1 - inset, y1 - inset))
    tight = tight.resize((tight.width * 8, tight.height * 8), Image.Resampling.NEAREST)
    tight = ImageEnhance.Contrast(tight).enhance(1.4)
    out2 = os.path.join(out_dir, "box1_user_photo_tight.png")
    tight.save(out2)
    print("saved", out2, tight.size)
