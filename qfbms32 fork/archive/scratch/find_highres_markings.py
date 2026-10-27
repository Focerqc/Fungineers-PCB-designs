import os
from PIL import Image

pcb_dir = r"c:\Users\quinn\Documents\GitHub\Fungineers PCB designs\qfbms32 ai pcb"
brain_dir = r"C:\Users\quinn\.gemini\antigravity-ide\brain\7bc5fde5-e6cf-413a-9764-f83c0e8df3ae"

# Let's inspect where this region is in IMG_0912 and IMG_0913
# We know R001 shunt resistor is very distinctive. Let's find it or crop around the MOSFET area
# In IMG_0912.jpg_crop.jpg, let's check its size and crop from it first
im12_crop_path = os.path.join(pcb_dir, "_reference", "crops", "IMG_0912.jpg_crop.jpg")
if os.path.exists(im12_crop_path):
    im12 = Image.open(im12_crop_path)
    print("im12_crop size:", im12.size)
    # Save a copy to brain or crop
    im12.save(os.path.join(brain_dir, "img12_crop_full.jpg"))

# Also in original IMG_0912.jpg, IMG_0913.jpg, IMG_0916.jpg
for fn in ["IMG_0912.jpg", "IMG_0913.jpg", "IMG_0916.jpg", "IMG_0923.jpg"]:
    p = os.path.join(pcb_dir, "_reference", "user_photos", fn)
    if os.path.exists(p):
        im = Image.open(p)
        print(fn, im.size)
