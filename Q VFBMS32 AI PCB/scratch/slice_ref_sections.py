from PIL import Image

p = r"c:\Users\quinn\Desktop\AI PCB CAD\Q VFBMS32 AI PCB\_reference\user_photos\image_3023b2.png"
im = Image.open(p)
print(f"Image format: {im.format}, size: {im.size}, mode: {im.mode}")

# Let's crop into 3 major sections:
# 1. Left power stage (XT30s, Shunts, MOSFETs, Fuse)
w, h = im.size
crop_left = im.crop((0, 0, int(w * 0.35), h))
crop_left.save(r"c:\Users\quinn\Desktop\AI PCB CAD\Q VFBMS32 AI PCB\scratch\zoom_power_stage.png")

# 2. Middle section (IC2, Buck, Boost, Inductor, Tantalum, IC1)
crop_mid = im.crop((int(w * 0.25), 0, int(w * 0.70), h))
crop_mid.save(r"c:\Users\quinn\Desktop\AI PCB CAD\Q VFBMS32 AI PCB\scratch\zoom_mid_stage.png")

# 3. Right section (ESP32, USB-C, U7, JSTs)
crop_right = im.crop((int(w * 0.65), 0, w, h))
crop_right.save(r"c:\Users\quinn\Desktop\AI PCB CAD\Q VFBMS32 AI PCB\scratch\zoom_right_stage.png")

print("Saved zoomed sections to scratch/")
