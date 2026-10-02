from PIL import Image

def crop_and_save(src, dst, pad=30):
    im = Image.open(src)
    bbox = im.getbbox()
    if bbox:
        crop = im.crop((max(0, bbox[0]-pad), max(0, bbox[1]-pad), min(im.width, bbox[2]+pad), min(im.height, bbox[3]+pad)))
        crop.save(dst)
        print(f"Saved {dst}: {crop.size}")

crop_and_save("scratch/test_verif_side.png", "scratch/crop_verif_side.png", pad=40)
crop_and_save("scratch/test_verif_top.png", "scratch/crop_verif_top.png", pad=40)

# Also let's crop a power-stage zoom of the top render
im_top = Image.open("scratch/crop_verif_top.png")
w, h = im_top.size
im_top.crop((0, 0, int(w * 0.35), h)).save("scratch/crop_verif_top_power.png")
print("Saved power zoom crop_verif_top_power.png")
