import os
from PIL import Image

pcb_dir = r"c:\Users\quinn\Documents\GitHub\Fungineers PCB designs\qfbms32 ai pcb"
brain_dir = r"C:\Users\quinn\.gemini\antigravity-ide\brain\7bc5fde5-e6cf-413a-9764-f83c0e8df3ae"

im16 = Image.open(os.path.join(pcb_dir, "_reference", "user_photos", "IMG_0916.jpg"))
w16, h16 = im16.size

# In IMG_0916, SSRelay is on the left (around x=0..600, y=1000..2500)
# Let's crop the region between SSRelay and BQ76952
crop16 = im16.crop((0, 500, int(w16 * 0.6), int(h16 * 0.7)))
crop16.save(os.path.join(brain_dir, "crop16_full_area.jpg"))

# Also in IMG_0912
im12 = Image.open(os.path.join(pcb_dir, "_reference", "user_photos", "IMG_0912.jpg"))
w12, h12 = im12.size
crop12 = im12.crop((int(w12 * 0.2), int(h12 * 0.1), int(w12 * 0.8), int(h12 * 0.6)))
crop12.save(os.path.join(brain_dir, "crop12_full_area.jpg"))

print("Cropped successfully!")
