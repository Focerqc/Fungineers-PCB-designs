from PIL import Image

im = Image.open("scratch/test_side_left.png")
bbox = im.getbbox()
if bbox:
    pad = 30
    crop = im.crop((bbox[0]-pad, bbox[1]-pad, bbox[2]+pad, bbox[3]+pad))
    crop.save("scratch/crop_side_left.png")
    print("Saved crop_side_left.png:", crop.size)
