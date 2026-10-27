from PIL import Image
import os

img_path = "_reference/vfbms32_cad_top_reference_rotated.png"
if os.path.exists(img_path):
    img = Image.open(img_path)
    print("vfbms32_cad_top_reference_rotated:", img.size)

for fname in ["vfbms32_real_top_hd.png", "vfbms32_v1_2_master_reference.png", "qfbms32_3d_top.png"]:
    p = os.path.join("_reference", fname) if "qfbms" not in fname else fname
    if os.path.exists(p):
        im = Image.open(p)
        print(fname, ":", im.size)
