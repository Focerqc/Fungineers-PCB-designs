import os
from PIL import Image

ref_path = '_reference/vfbms32_cad_top_reference_rotated.png'
img = Image.open(ref_path)
print("CAD Ref Size:", img.size)

w_mm, h_mm = 130.0, 32.0
iw, ih = img.size

# Let's crop X=20 to 42mm, Y=0 to 15mm
x0 = int((20.0 / w_mm) * iw)
x1 = int((42.0 / w_mm) * iw)
y0 = int((0.0 / h_mm) * ih)
y1 = int((15.0 / h_mm) * ih)

crop = img.crop((x0, y0, x1, y1))
crop.save('scratch/cad_ref_crop.png')
print("Saved CAD crop")
