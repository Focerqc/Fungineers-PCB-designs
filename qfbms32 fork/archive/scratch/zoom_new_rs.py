from PIL import Image

im = Image.open("qfbms32 ai pcb/qfbms32_3d_top.png")
w, h = im.size
cx = int((17.5 / 130.0) * w)
cy = int((16.0 / 32.0) * h)
crop = im.crop((cx - 100, cy - 80, cx + 100, cy + 80))
crop.save("qfbms32 ai pcb/scratch/zoom_new_rs1_rs2.png")
print("Saved zoom_new_rs1_rs2.png")
