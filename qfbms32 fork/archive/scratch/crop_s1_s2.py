from PIL import Image

# 1. 3d top
im_3d = Image.open("qfbms32 ai pcb/qfbms32_3d_top.png")
w_3d, h_3d = im_3d.size
# board is 130mm x 32mm
# (17.5, 16.0) is at x = 17.5/130 * w, y = 16.0/32 * h
cx_3d = int((17.5 / 130.0) * w_3d)
cy_3d = int((16.0 / 32.0) * h_3d)
crop_3d = im_3d.crop((cx_3d - 100, cy_3d - 80, cx_3d + 100, cy_3d + 80))
crop_3d.save("qfbms32 ai pcb/scratch/crop_3d_s1_s2.png")
print("Saved crop_3d_s1_s2.png")

# 2. real top hd
im_real = Image.open("qfbms32 ai pcb/_reference/vfbms32_real_top_hd.png")
w_r, h_r = im_real.size
cx_r = int((17.5 / 130.0) * w_r)
cy_r = int((16.0 / 32.0) * h_r)
crop_r = im_real.crop((max(0, cx_r - 200), max(0, cy_r - 150), min(w_r, cx_r + 200), min(h_r, cy_r + 150)))
crop_r.save("qfbms32 ai pcb/scratch/crop_real_s1_s2.png")
print("Saved crop_real_s1_s2.png")

# 3. cad reference
im_cad = Image.open("qfbms32 ai pcb/_reference/vfbms32_cad_top_reference_rotated.png")
w_c, h_c = im_cad.size
cx_c = int((17.5 / 130.0) * w_c)
cy_c = int((16.0 / 32.0) * h_c)
crop_cad = im_cad.crop((max(0, cx_c - 150), max(0, cy_c - 100), min(w_c, cx_c + 150), min(h_c, cy_c + 100)))
crop_cad.save("qfbms32 ai pcb/scratch/crop_cad_s1_s2.png")
print("Saved crop_cad_s1_s2.png")
