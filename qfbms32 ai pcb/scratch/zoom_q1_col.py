import os
from PIL import Image

pcb_dir = r"c:\Users\quinn\Documents\GitHub\Fungineers PCB designs\qfbms32 ai pcb"
brain_dir = r"C:\Users\quinn\.gemini\antigravity-ide\brain\7bc5fde5-e6cf-413a-9764-f83c0e8df3ae"

im12 = Image.open(os.path.join(pcb_dir, "_reference", "user_photos", "IMG_0912.jpg"))
w, h = im12.size

# In crop12_full_area, Q1 is on the left, R001 is in the center
# Let's crop right around the column between Q1 and R001/SSRelay
# In IMG_0912 original:
# crop12 was: (int(w * 0.2), int(h * 0.1), int(w * 0.8), int(h * 0.6))
# Q1 and R001 are around the middle of that crop
base_x = int(w * 0.2)
base_y = int(h * 0.1)

# Let's crop tightly around the column of components next to Q1
# Let's make 2 crops:
# 1. Column between Q1 and R001/JST
# 2. Area between Q1 and SSRelay
crop_zoom1 = im12.crop((base_x + 250, base_y + 400, base_x + 950, base_y + 1300))
crop_zoom1.save(os.path.join(brain_dir, "zoom_q1_column.jpg"))

print("Saved zoom_q1_column.jpg")
