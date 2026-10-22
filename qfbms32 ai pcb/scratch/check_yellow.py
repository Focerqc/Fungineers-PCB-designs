from PIL import Image

def find_yellow(path):
    im = Image.open(path)
    print(path, "size:", im.size)
    w, h = im.size
    yellow_pts = []
    for y in range(h):
        for x in range(w):
            r, g, b, a = im.getpixel((x, y))
            if a > 100 and r > 150 and g > 130 and b < 50:
                yellow_pts.append((x, y))
    if yellow_pts:
        xs = [p[0] for p in yellow_pts]
        ys = [p[1] for p in yellow_pts]
        print(f"  Yellow pixels: {len(yellow_pts)}")
        print(f"  X range: [{min(xs)}, {max(xs)}], Y range: [{min(ys)}, {max(ys)}]")
    else:
        print("  NO YELLOW PIXELS FOUND")

find_yellow("scratch/test_side_left.png")
find_yellow("scratch/test_side_z25.png")
