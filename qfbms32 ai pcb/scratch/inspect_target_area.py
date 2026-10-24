from PIL import Image
import os

# Let's crop CAD reference around X=30.8, Y=28
cad_img = Image.open("_reference/vfbms32_cad_top_reference_rotated.png")
# scale: 813 / 130 = 6.2538, 200 / 32 = 6.25
cx = int(30.85 * (813.0 / 130.0))
cy = int(28.2 * (200.0 / 32.0))
cad_crop = cad_img.crop((cx - 40, cy - 40, cx + 40, cy + 40))
cad_crop.save("scratch/crop_target_cad.png")
print("Saved CAD crop")

# Let's inspect crops in _reference/crops
for fn in os.listdir("_reference/crops"):
    if fn.endswith((".jpg", ".png")):
        fp = os.path.join("_reference/crops", fn)
        im = Image.open(fp)
        print(f"Crop {fn}: size {im.size}")
