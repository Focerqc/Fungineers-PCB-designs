import os
from PIL import Image

img_path = 'qfbms32 ai pcb/_reference/vfbms32_real_top_hd.png'
if not os.path.exists(img_path):
    img_path = '_reference/vfbms32_real_top_hd.png'

img = Image.open(img_path)
print("Image size:", img.size)

# The board is 130mm x 32mm.
# Let's crop X: 15mm to 40mm, Y: 0mm to 12mm
w_mm, h_mm = 130.0, 32.0
iw, ih = img.size

x0 = int((15.0 / w_mm) * iw)
x1 = int((42.0 / w_mm) * iw)
y0 = int((0.0 / h_mm) * ih)
y1 = int((14.0 / h_mm) * ih)

crop = img.crop((x0, y0, x1, y1))
os.makedirs('scratch', exist_ok=True)
crop.save('scratch/crop_q1_ssr.png')
print("Saved crop to scratch/crop_q1_ssr.png with size", crop.size)
