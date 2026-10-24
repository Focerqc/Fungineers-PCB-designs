from PIL import Image

# Let's inspect where Q1/SSR is in IMG_0916
im = Image.open('_reference/user_photos/IMG_0916.jpg')
w, h = im.size

# Let's crop center
crop1 = im.crop((w*0.2, h*0.2, w*0.8, h*0.8))
crop1.thumbnail((800, 800))
crop1.save('scratch/img_0916_center.jpg')
print("Done")
