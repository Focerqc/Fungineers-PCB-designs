from PIL import Image

im = Image.open("scratch/crop_v12_can.png")
# let's zoom in 3x
w, h = im.size
crop = im.crop((int(w * 0.1), int(h * 0.1), int(w * 0.8), int(h * 0.8)))
crop = crop.resize((crop.width * 3, crop.height * 3), Image.NEAREST)
crop.save("scratch/crop_v12_zoom.png")
