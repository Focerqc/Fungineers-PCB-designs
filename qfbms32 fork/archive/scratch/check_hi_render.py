import os
from PIL import Image

brain_dir = r"C:\Users\quinn\.gemini\antigravity-ide\brain\7bc5fde5-e6cf-413a-9764-f83c0e8df3ae"
pcb_dir = r"c:\Users\quinn\Documents\GitHub\Fungineers PCB designs\qfbms32 ai pcb"

# Render a higher resolution top crop directly with kicad-cli or inspect raw
# In raw_top_png, let's see its size
raw_path = os.path.join(pcb_dir, "qfbms32_layout_top_hi_raw.png")
im = Image.open(raw_path)
print("raw_top size:", im.size)
w, h = im.size

# X: 27..32mm, Y: 3..18mm
x0 = int((27.0 / 130.0) * w)
x1 = int((32.0 / 130.0) * w)
y0 = int((3.0 / 32.0) * h)
y1 = int((19.0 / 32.0) * h)

crop_hi = im.crop((x0, y0, x1, y1))
crop_hi.save(os.path.join(brain_dir, "zoom_new_0603_hi.png"))
print("Saved zoom_new_0603_hi.png")
