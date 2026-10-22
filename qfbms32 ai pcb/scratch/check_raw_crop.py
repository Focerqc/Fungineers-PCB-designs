from PIL import Image

im = Image.open(r'c:\Users\quinn\Desktop\AI PCB CAD\raw_left_crop.png')
w, h = im.size

def find_first(y):
    for x in range(w):
        r, g, b, a = im.getpixel((x, y))
        if a > 50:
            return x, (r, g, b)
    return None, None

print(f"Image height: {h}")
print("PCB middle (between connectors, y=170..190):")
for y in [170, 180, 190]:
    x, col = find_first(y)
    print(f"y={y}: x={x}, col={col}")

print("Female XT30 (y=40..100):")
for y in range(40, 110, 10):
    x, col = find_first(y)
    print(f"y={y}: x={x}, col={col}")

print("Male XT30 (y=260..320):")
for y in range(260, 330, 10):
    x, col = find_first(y)
    print(f"y={y}: x={x}, col={col}")
