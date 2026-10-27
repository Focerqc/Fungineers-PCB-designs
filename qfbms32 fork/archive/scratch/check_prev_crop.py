from PIL import Image

im = Image.open(r'c:\Users\quinn\Desktop\AI PCB CAD\prev_labeled_crop.png')
w, h = im.size

def find_first(y):
    for x in range(w):
        r, g, b, a = im.getpixel((x, y))
        # background is dark slate (22, 27, 34)
        if (r, g, b) != (22, 27, 34):
            return x, (r, g, b)
    return None, None

print("=== Middle of board (PCB Edge) around y=180..220 ===")
for y in [190, 200, 210]:
    x, col = find_first(y)
    print(f"y={y}: x={x}, col={col}")

print("=== Top Connector (XT30PW-F) around y=50..130 ===")
for y in range(60, 130, 10):
    x, col = find_first(y)
    print(f"y={y}: x={x}, col={col}")

print("=== Bottom Connector (XT30PW-M) around y=250..330 ===")
for y in range(250, 330, 10):
    x, col = find_first(y)
    print(f"y={y}: x={x}, col={col}")
