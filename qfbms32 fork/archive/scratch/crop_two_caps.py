import os
from PIL import Image

pcb_dir = r"c:\Users\quinn\Documents\GitHub\Fungineers PCB designs\qfbms32 ai pcb"
im12 = Image.open(os.path.join(pcb_dir, "_reference", "user_photos", "IMG_0912.jpg"))
w, h = im12.size

base_x = int(w * 0.2)
base_y = int(h * 0.1)

# Crop the top area next to Q1 (where the two capacitors are)
# In zoom_q1_column, the top of the column was base_y + 400.
# Let's crop from base_y + 200 to base_y + 800, base_x + 300 to base_x + 900
crop_caps = im12.crop((base_x + 350, base_y + 250, base_x + 850, base_y + 750))
crop_caps.save("scratch/zoom_two_caps.jpg")
print("Saved scratch/zoom_two_caps.jpg, size:", crop_caps.size)
