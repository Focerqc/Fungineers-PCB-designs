import os
from PIL import Image

pcb_dir = r"c:\Users\quinn\Documents\GitHub\Fungineers PCB designs\qfbms32 ai pcb"
brain_dir = r"C:\Users\quinn\.gemini\antigravity-ide\brain\7bc5fde5-e6cf-413a-9764-f83c0e8df3ae"

real = Image.open(os.path.join(pcb_dir, "_reference", "vfbms32_real_top_hd.png"))
rw, rh = real.size

# X=29.75, Y=17.20
# Let's crop X: 27..32mm, Y: 13..20mm in real_top_hd
cx = int((29.75 / 130.0) * rw)
cy = int((17.20 / 32.0) * rh)
rx = int((3.0 / 130.0) * rw)
ry = int((3.0 / 32.0) * rh)

crop_bot = real.crop((cx - rx, cy - ry, cx + rx, cy + ry))
crop_bot_5x = crop_bot.resize((crop_bot.width * 5, crop_bot.height * 5), Image.Resampling.NEAREST)
crop_bot_5x.save(os.path.join(brain_dir, "real_y17_2_zoom.png"))

# Also crop Y=7.6 and Y=8.95 in real_top_hd
cy_mid = int((8.25 / 32.0) * rh)
crop_mid = real.crop((cx - rx, cy_mid - ry, cx + rx, cy_mid + ry))
crop_mid_5x = crop_mid.resize((crop_mid.width * 5, crop_mid.height * 5), Image.Resampling.NEAREST)
crop_mid_5x.save(os.path.join(brain_dir, "real_y8_25_zoom.png"))

print("Cropped real_top_hd successfully!")
