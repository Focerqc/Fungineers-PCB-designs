from PIL import Image

im = Image.open(r"c:\Users\quinn\Desktop\AI PCB CAD\Q VFBMS32 AI PCB\_reference\user_photos\image_3023b2.png")
w, h = im.size

# Let's crop strips at the 4 edges to locate the black PCB boundaries
# PCB is dark black/green, wood background is light brown.
print("Sampling image:")
# Sample left, right, top, bottom:
# Top edge: look down column at x = 500
col = [im.getpixel((500, y)) for y in range(h)]
# Find where dark PCB starts
for y in range(h):
    r, g, b, *a = im.getpixel((500, y))
    # Wood is bright (r>100, g>80), PCB is dark (r<50, g<50, b<50)
    if r < 60 and g < 60 and b < 60:
        top_y = y
        break

for y in range(h-1, -1, -1):
    r, g, b, *a = im.getpixel((500, y))
    if r < 60 and g < 60 and b < 60:
        bot_y = y
        break

print(f"Detected PCB top_y ~ {top_y}, bot_y ~ {bot_y}, height ~ {bot_y - top_y} px")

# Left edge: at y = 150
for x in range(w):
    r, g, b, *a = im.getpixel((x, 150))
    if r < 60 and g < 60 and b < 60:
        left_x = x
        break

for x in range(w-1, -1, -1):
    r, g, b, *a = im.getpixel((x, 150))
    if r < 60 and g < 60 and b < 60:
        right_x = x
        break

print(f"Detected PCB left_x ~ {left_x}, right_x ~ {right_x}, width ~ {right_x - left_x} px")

px_per_mm_x = (right_x - left_x) / 130.0
px_per_mm_y = (bot_y - top_y) / 32.0
print(f"Scale: {px_per_mm_x:.2f} px/mm (X), {px_per_mm_y:.2f} px/mm (Y)")
