from PIL import Image

cad_img = Image.open(r"c:\Users\quinn\Documents\GitHub\Fungineers PCB designs\Q VFBMS32 AI PCB\_reference\vfbms32_cad_top_reference_rotated.png")
# 813 x 200
# 0 to 130 mm, 0 to 32 mm
scale_x = cad_img.width / 130.0
scale_y = cad_img.height / 32.0

# Crop around X = 5..18 mm, Y = 10..24 mm
box_cad = (int(4.0 * scale_x), int(10.0 * scale_y), int(18.0 * scale_x), int(24.0 * scale_y))
crop_cad = cad_img.crop(box_cad)
crop_cad.save(r"c:\Users\quinn\Documents\GitHub\Fungineers PCB designs\Q VFBMS32 AI PCB\scratch\crop_cad_target.png")
print("Saved crop_cad_target.png, size:", crop_cad.size)

# If 3d top exists:
try:
    top_3d = Image.open(r"c:\Users\quinn\Documents\GitHub\Fungineers PCB designs\Q VFBMS32 AI PCB\VFBMS32_3d_top.png")
    scale_3d_x = top_3d.width / 130.0
    scale_3d_y = top_3d.height / 32.0
    crop_3d = top_3d.crop((int(4.0 * scale_3d_x), int(10.0 * scale_3d_y), int(18.0 * scale_3d_x), int(24.0 * scale_3d_y)))
    crop_3d.save(r"c:\Users\quinn\Documents\GitHub\Fungineers PCB designs\Q VFBMS32 AI PCB\scratch\crop_3d_target.png")
    print("Saved crop_3d_target.png, size:", crop_3d.size)
except Exception as e:
    print("3D error:", e)

# If real top exists:
try:
    real_top = Image.open(r"c:\Users\quinn\Documents\GitHub\Fungineers PCB designs\Q VFBMS32 AI PCB\_reference\vfbms32_real_top_hd.png")
    scale_rt_x = real_top.width / 130.0
    scale_rt_y = real_top.height / 32.0
    crop_rt = real_top.crop((int(4.0 * scale_rt_x), int(10.0 * scale_rt_y), int(18.0 * scale_rt_x), int(24.0 * scale_rt_y)))
    crop_rt.save(r"c:\Users\quinn\Documents\GitHub\Fungineers PCB designs\Q VFBMS32 AI PCB\scratch\crop_real_target.png")
    print("Saved crop_real_target.png, size:", crop_rt.size)
except Exception as e:
    print("Real error:", e)
