import os
from PIL import Image, ImageEnhance

pcb_dir = r"c:\Users\quinn\Documents\GitHub\Fungineers PCB designs\qfbms32 ai pcb"
brain_dir = r"C:\Users\quinn\.gemini\antigravity-ide\brain\7bc5fde5-e6cf-413a-9764-f83c0e8df3ae"

im12 = Image.open(os.path.join(pcb_dir, "_reference", "user_photos", "IMG_0912.jpg"))
w, h = im12.size

base_x = int(w * 0.2)
base_y = int(h * 0.1)

# In zoom_q1_column, base_x + 250..950, base_y + 400..1300
# Let's crop a bit lower to see below C_DISC (down to base_y + 1800)
crop_full_col = im12.crop((base_x + 200, base_y + 350, base_x + 1000, base_y + 1750))
crop_full_col.save(os.path.join(brain_dir, "col_full_img12.jpg"))

# Let's zoom into individual components in this column
# 1. Top component (near Y=4.05)
c_top = im12.crop((base_x + 480, base_y + 450, base_x + 650, base_y + 550))
c_top.save(os.path.join(brain_dir, "part_y4_05.jpg"))

# 2. Middle components (near Y=7.60 and Y=8.95)
c_mid = im12.crop((base_x + 450, base_y + 650, base_x + 650, base_y + 850))
c_mid.save(os.path.join(brain_dir, "parts_y7_y9.jpg"))

# 3. Bottom component (below C_DISC, near Y=17.20)
c_bot = im12.crop((base_x + 450, base_y + 1050, base_x + 750, base_y + 1450))
c_bot.save(os.path.join(brain_dir, "part_below_cdisc.jpg"))

print("Cropped individual components!")
