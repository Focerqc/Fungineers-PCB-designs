from PIL import Image
import numpy as np

img = Image.open("_reference/vfbms32_cad_top_reference_rotated.png").convert("RGBA")
arr = np.array(img)
# find non-transparent or non-white/black bounding box
# let's find alpha > 0 or background color
print("Shape:", arr.shape)

# Let's crop around Box 1: x=13.4, y=30.7, w=2.9, h=1.5
# and Box 2: x=15.1, y=1.13, w=3.2, h=1.6
# In 130mm x 32mm:
# 813 / 130 = 6.2538 px/mm
# 200 / 32 = 6.25 px/mm
# Let's check aspect ratio: 813 / 200 = 4.065. 130 / 32 = 4.0625! They match almost exactly!
# Let's crop around (13.4, 30.7) and (15.1, 1.13)
def mm_to_px(x, y):
    return int(x * (813.0 / 130.0)), int(y * (200.0 / 32.0))

c1_x, c1_y = mm_to_px(13.4, 30.7)
c2_x, c2_y = mm_to_px(15.1, 1.125)

print(f"C1 px: ({c1_x}, {c1_y})")
print(f"C2 px: ({c2_x}, {c2_y})")

# Let's save crops
crop1 = img.crop((max(0, c1_x - 50), max(0, c1_y - 50), min(813, c1_x + 50), min(200, c1_y + 50)))
crop1.save("scratch/crop_box1_cad.png")

crop2 = img.crop((max(0, c2_x - 50), max(0, c2_y - 50), min(813, c2_x + 50), min(200, c2_y + 50)))
crop2.save("scratch/crop_box2_cad.png")
print("Saved crops")
