import os
from PIL import Image

ref_path = r"c:\Users\quinn\Desktop\AI PCB CAD\Q VFBMS32 AI PCB\_reference\vfbms32_v1_2_master_reference.png"
img = Image.open(ref_path)
w, h = img.size

# Let's inspect rows and columns to find PCB boundaries
# The PCB is black/dark green, background is wooden table (brownish/light)
# Let's sample pixels across horizontal and vertical profiles

print(f"Image size: {w}x{h}")

# Let's find PCB left, right, top, bottom
# Wooden table is yellowish/brownish (R > 100, G > 80, B > 50, and R > B + 30)
# PCB is dark (R < 80, G < 80, B < 80)
# Let's do a quick scan
for y in [50, 100, 150, 200]:
    row = [img.getpixel((x, y)) for x in range(w)]
    # find where dark starts and ends
    dark_indices = [x for x, px in enumerate(row) if (px[0] < 80 and px[1] < 80 and px[2] < 80)]
    if dark_indices:
        print(f"Y={y}: dark span {min(dark_indices)} to {max(dark_indices)}")

# Also top/bottom at x=200, 500, 800
for x in [200, 500, 800]:
    col = [img.getpixel((x, y)) for y in range(h)]
    dark_indices = [y for y, px in enumerate(col) if (px[0] < 80 and px[1] < 80 and px[2] < 80)]
    if dark_indices:
        print(f"X={x}: dark span {min(dark_indices)} to {max(dark_indices)}")
