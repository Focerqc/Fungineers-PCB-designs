import os
from PIL import Image, ImageDraw

ref_path = r"c:\Users\quinn\Desktop\AI PCB CAD\Q VFBMS32 AI PCB\_reference\vfbms32_v1_2_master_reference.png"
img = Image.open(ref_path)

# Let's crop x: 20 to 320, y: 25 to 265
crop = img.crop((20, 25, 340, 265)).convert("RGB")
draw = ImageDraw.Draw(crop)

# Let's draw grid lines every 20 pixels with labels
for x in range(0, crop.width, 20):
    draw.line([(x, 0), (x, crop.height)], fill=(255, 0, 0, 100), width=1)
    draw.text((x+1, 2), f"{x}", fill=(255, 255, 0))

for y in range(0, crop.height, 20):
    draw.line([(0, y), (crop.width, y)], fill=(0, 255, 0, 100), width=1)
    draw.text((2, y+1), f"{y}", fill=(0, 255, 255))

out_path = r"c:\Users\quinn\Desktop\AI PCB CAD\Q VFBMS32 AI PCB\scratch\power_stage_grid.png"
crop.save(out_path)
print("Saved power stage grid:", out_path)
