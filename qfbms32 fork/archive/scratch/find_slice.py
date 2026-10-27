import os
from PIL import Image

pcb_dir = r"c:\Users\quinn\Documents\GitHub\Fungineers PCB designs\qfbms32 ai pcb"
im12 = Image.open(os.path.join(pcb_dir, "_reference", "user_photos", "IMG_0912.jpg"))
w, h = im12.size

# In IMG_0912, let's find the whole board across width
# Let's save a grid of 4 horizontal slices across the top edge
slice_w = int(w * 0.15)
for i in range(5):
    x_start = int(w * (0.05 + i * 0.12))
    crop = im12.crop((x_start, int(h * 0.15), x_start + slice_w, int(h * 0.45)))
    crop.save(f"scratch/slice_{i}.jpg")
    print(f"Slice {i} from x={x_start}")
