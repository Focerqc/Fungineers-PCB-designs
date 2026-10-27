from PIL import Image

# In IMG_0912.jpg_crop.jpg: size (1200, 1599)
# In our earlier view of IMG_0912, the JST connectors are in the upper-right / middle.
im12 = Image.open("_reference/crops/IMG_0912.jpg_crop.jpg")
# let's crop the area around CAN connector
w, h = im12.size
# CAN connector is around x: 500..800, y: 150..500
c12 = im12.crop((int(w * 0.45), int(h * 0.1), int(w * 0.85), int(h * 0.45)))
c12.save("scratch/crop_img0912_can.png")

# In vfbms32_v1_2_master_reference.png: size (944, 291)
# 130mm x 32mm board
im_v12 = Image.open("_reference/vfbms32_v1_2_master_reference.png")
w, h = im_v12.size
# x=30.85 / 130 = 0.237, y=28.2 / 32 = 0.88
cx = int(0.237 * w)
cy = int(0.88 * h)
c_v12 = im_v12.crop((max(0, cx - 80), max(0, cy - 80), min(w, cx + 80), min(h, cy + 80)))
c_v12.save("scratch/crop_v12_can.png")

# In vfbms32_real_top_hd.png: size (894, 276)
im_real = Image.open("_reference/vfbms32_real_top_hd.png")
w, h = im_real.size
cx = int(0.237 * w)
cy = int(0.88 * h)
c_real = im_real.crop((max(0, cx - 80), max(0, cy - 80), min(w, cx + 80), min(h, cy + 80)))
c_real.save("scratch/crop_real_can.png")
print("Saved comparison crops")
