from PIL import Image

im = Image.open("scratch/test_side_z25.png")
# Let's inspect where pixels are non-transparent
print("Image size:", im.size)
bbox = im.getbbox()
print("bbox:", bbox)
crop = im.crop((bbox[0]-10, bbox[1]-10, bbox[2]+10, bbox[3]+10))
crop.save("scratch/crop_side_z25_full.png")
print("Saved crop_side_z25_full.png:", crop.size)
