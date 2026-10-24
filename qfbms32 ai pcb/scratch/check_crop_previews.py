import os
from PIL import Image

pcb_dir = r"c:\Users\quinn\Documents\GitHub\Fungineers PCB designs\qfbms32 ai pcb"
brain_dir = r"C:\Users\quinn\.gemini\antigravity-ide\brain\7bc5fde5-e6cf-413a-9764-f83c0e8df3ae"

# Let's inspect img0913_crop.png
p13 = os.path.join(pcb_dir, "_reference", "crops", "img0913_crop.png")
if os.path.exists(p13):
    im13 = Image.open(p13)
    print("img0913_crop size:", im13.size)
    # Let's save a downscaled preview to brain
    im13_small = im13.resize((800, int(800 * im13.height / im13.width)))
    im13_small.save(os.path.join(brain_dir, "img13_preview.png"))

p12 = os.path.join(pcb_dir, "_reference", "crops", "IMG_0912.jpg_crop.jpg")
if os.path.exists(p12):
    im12 = Image.open(p12)
    print("im12 size:", im12.size)
    im12_small = im12.resize((800, int(800 * im12.height / im12.width)))
    im12_small.save(os.path.join(brain_dir, "img12_preview.jpg"))
