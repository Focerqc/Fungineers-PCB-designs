from PIL import Image

im = Image.open('_reference/user_photos/image_3023b2.png')
print("Format:", im.format, "Mode:", im.mode, "Size:", im.size)
# Let's save a copy to scratch
im.save('scratch/user_image_3023b2.png')
