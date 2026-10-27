from PIL import Image

im = Image.open("_reference/crops/mosfets_top_hd.png")
# let's crop top left
w, h = im.size
crop = im.crop((0, 0, int(w * 0.4), int(h * 0.4)))
crop.save("scratch/crop_mosfets_top_left.png")
