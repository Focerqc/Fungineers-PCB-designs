from PIL import Image

im = Image.open(r'c:\Users\quinn\Desktop\AI PCB CAD\raw_left_crop.png')
w, h = im.size

# Let's scan horizontally across the female connector at y=70 (center of female connector)
print("Scanning across female connector at y=70:")
for x in range(30, 150, 5):
    r, g, b, a = im.getpixel((x, 70))
    print(f"x={x}: col=({r}, {g}, {b}, {a})")

print("\nScanning across male connector at y=290:")
for x in range(25, 150, 5):
    r, g, b, a = im.getpixel((x, 290))
    print(f"x={x}: col=({r}, {g}, {b}, {a})")
