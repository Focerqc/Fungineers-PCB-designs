from PIL import Image

im = Image.open(r'c:\Users\quinn\Desktop\AI PCB CAD\Q VFBMS32 AI PCB\VFBMS32_layout_top_hi_raw.png')
print("VFBMS32_layout_top_hi_raw size:", im.size)
# The raw image has the board rendered directly by kicad-cli
# Let's crop the left edge
crop = im.crop((0, 0, 400, im.height))
crop.save(r'c:\Users\quinn\Desktop\AI PCB CAD\raw_left_crop.png')
print("Saved raw_left_crop.png")
