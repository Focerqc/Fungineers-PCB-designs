from PIL import Image

im = Image.open("VFBMS32_layout_top_hi_raw.png")
bbox = im.getbbox()
if bbox:
    cropped = im.crop(bbox)
    # Resize to clean dimensions for dashboard
    cropped.save("VFBMS32_3d_top.png")
    print(f"Updated VFBMS32_3d_top.png: {cropped.size}")
