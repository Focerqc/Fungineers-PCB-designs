from PIL import Image

# Let's crop user photo IMG_0916 where U7 is
img = Image.open('_reference/user_photos/IMG_0916.jpg')
w, h = img.size

# Let's find where ESP32 is in IMG_0916
# Let's save a series of crops across the board to locate it
for i in range(4):
    crop = img.crop((int(w * (0.25 * i)), int(h * 0.25), int(w * (0.25 * (i+1))), int(h * 0.75)))
    crop.save(f'scratch/img0916_quad_{i}.png')
print("Saved img0916 quads")
