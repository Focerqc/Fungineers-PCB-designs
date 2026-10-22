from PIL import Image

# Check quad 3 (right side of image)
for i in [2, 3]:
    im = Image.open(f'scratch/img0916_quad_{i}.png')
    print(f"Quad {i} size: {im.size}")

# Let's crop quad 3 around center
im3 = Image.open('scratch/img0916_quad_3.png')
w, h = im3.size
crop_esp_u7 = im3.crop((int(w * 0.1), int(h * 0.2), int(w * 0.9), int(h * 0.8)))
crop_esp_u7.save('scratch/img0916_esp_u7_close.png')
print("Saved img0916_esp_u7_close.png")
