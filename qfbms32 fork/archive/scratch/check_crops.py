from PIL import Image

for fn in ["IMG_0912.jpg_crop.jpg", "IMG_0916.jpg_crop.jpg", "crop_mid1.jpg"]:
    im = Image.open(f"_reference/crops/{fn}")
    w, h = im.size
    # let's crop around the CAN connector / MOSFET area
    # In IMG_0912, the CAN connector is visible next to the MOSFETs
    print(fn, im.size)
