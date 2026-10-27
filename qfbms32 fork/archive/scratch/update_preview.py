import os
import sys
from PIL import Image
sys.path.insert(0, os.getcwd())
import generate_annotated_preview

# Crop raw image
raw_path = "qfbms32_layout_top_hi_raw.png"
if os.path.exists(raw_path):
    im = Image.open(raw_path)
    bbox = im.getbbox()
    if bbox:
        pad = 30
        box = (max(0, bbox[0]-pad), max(0, bbox[1]-pad), min(im.width, bbox[2]+pad), min(im.height, bbox[3]+pad))
        im.crop(box).save(raw_path)
        print(f"Cropped raw image to {im.crop(box).size}")

# Update generate_annotated_preview brain dir to current conversation
current_brain = r"C:\Users\quinn\.gemini\antigravity-ide\brain\dd3e1d3a-3b25-4800-9f81-37526309b7a2"
os.makedirs(current_brain, exist_ok=True)
generate_annotated_preview.generate_annotated_preview()

# Also copy to current brain dir
import shutil
shutil.copy("qfbms32_layout_labeled.png", os.path.join(current_brain, "qfbms32_layout_labeled.png"))
shutil.copy("qfbms32_3d_top.png", os.path.join(current_brain, "qfbms32_3d_top.png"))
print("Done updating previews and copying to current brain")
