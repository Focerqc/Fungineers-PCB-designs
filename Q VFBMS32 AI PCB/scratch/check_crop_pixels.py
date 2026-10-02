from PIL import Image

im = Image.open(r'c:\Users\quinn\Desktop\AI PCB CAD\test_crop.png')
w, h = im.size

# Let's inspect rows from top to bottom
# Top connector is around y = 30..80
# PCB middle (between connectors) is around y = 100..120
# Bottom connector is around y = 140..190

def find_first_non_transparent(y):
    for x in range(w):
        r, g, b, a = im.getpixel((x, y))
        if a > 50:
            return x, (r, g, b, a)
    return None, None

print("=== Middle of board (PCB Edge) ===")
for y in [105, 110, 115]:
    x, col = find_first_non_transparent(y)
    print(f"y={y}: first x={x}, col={col}")

print("=== Top Connector (XT30PW-F) ===")
for y in range(30, 80, 5):
    x, col = find_first_non_transparent(y)
    print(f"y={y}: first x={x}, col={col}")

print("=== Bottom Connector (XT30PW-M) ===")
for y in range(140, 190, 5):
    x, col = find_first_non_transparent(y)
    print(f"y={y}: first x={x}, col={col}")
