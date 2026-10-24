from PIL import Image

im = Image.open("qfbms32 ai pcb/_reference/vfbms32_real_top_hd.png")
w, h = im.size

# Let's find the exact pixel coords
# Board in image: let's inspect the whole image bounding box or crop around x: 16mm..19mm, y: 13mm..18mm
# Board length is 130mm, height 32mm
# In vfbms32_real_top_hd.png, let's find the board bounds
import numpy as np
arr = np.array(im)
print("Image shape:", arr.shape)

# Let's crop x in [0.10, 0.18] * w, y in [0.35, 0.65] * h
x0 = int(0.11 * w)
x1 = int(0.18 * w)
y0 = int(0.35 * h)
y1 = int(0.65 * h)

crop = im.crop((x0, y0, x1, y1))
crop.save("qfbms32 ai pcb/scratch/zoom_s1_s2_real.png")
print("Saved zoom_s1_s2_real.png")
