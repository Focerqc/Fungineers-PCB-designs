import os
from PIL import Image

pcb_dir = r"c:\Users\quinn\Documents\GitHub\Fungineers PCB designs\qfbms32 ai pcb"
brain_dir = r"C:\Users\quinn\.gemini\antigravity-ide\brain\7bc5fde5-e6cf-413a-9764-f83c0e8df3ae"

for fn in ["IMG_0916.jpg", "IMG_0923.jpg", "IMG_0927.jpg"]:
    p = os.path.join(pcb_dir, "_reference", "user_photos", fn)
    if os.path.exists(p):
        im = Image.open(p)
        w, h = im.size
        # downscale to max 1000px
        scale = min(1000/w, 1000/h)
        im_small = im.resize((int(w * scale), int(h * scale)))
        im_small.save(os.path.join(brain_dir, f"{fn}_preview.jpg"))
        print(f"Saved {fn}_preview.jpg")
