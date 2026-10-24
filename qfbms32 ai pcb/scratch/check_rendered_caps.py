from PIL import Image

im = Image.open('qfbms32_3d_top.png')
w, h = im.size

# Board is 130mm x 32mm
# We want X: 25 to 35 mm, Y: 0 to 8 mm
x0 = int((25.0 / 130.0) * w)
x1 = int((35.0 / 130.0) * w)
y0 = int((0.0 / 32.0) * h)
y1 = int((8.0 / 32.0) * h)

crop = im.crop((x0, y0, x1, y1))
crop.save('scratch/crop_rendered_two_caps.png')
print("Render crop saved, size:", crop.size)
