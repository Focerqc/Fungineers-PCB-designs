from PIL import Image

im = Image.open(r'c:\Users\quinn\Desktop\AI PCB CAD\raw_left_crop.png')
w, h = im.size

top_y = 38
scale = 8.875
pcb_left_x = 38

print("=== Female Connector (Y from 40 to 120): ===")
for y in range(40, 130, 5):
    first_yellow_x = None
    for x in range(w):
        r, g, b, a = im.getpixel((x, y))
        if a > 100 and r > 150 and g > 150 and b < 100:
            first_yellow_x = x
            break
    if first_yellow_x is not None:
        diff_mm = (first_yellow_x - pcb_left_x) / scale
        print(f"y={y:3d} (Y_mm={(y-top_y)/scale:5.2f}mm): first_yellow_x={first_yellow_x:3d}, diff={diff_mm:+.3f} mm")
    else:
        print(f"y={y:3d} (Y_mm={(y-top_y)/scale:5.2f}mm): NO YELLOW")

print("\n=== Male Connector (Y from 240 to 320): ===")
for y in range(240, 325, 5):
    first_yellow_x = None
    for x in range(w):
        r, g, b, a = im.getpixel((x, y))
        if a > 100 and r > 150 and g > 150 and b < 100:
            first_yellow_x = x
            break
    if first_yellow_x is not None:
        diff_mm = (first_yellow_x - pcb_left_x) / scale
        print(f"y={y:3d} (Y_mm={(y-top_y)/scale:5.2f}mm): first_yellow_x={first_yellow_x:3d}, diff={diff_mm:+.3f} mm")
    else:
        print(f"y={y:3d} (Y_mm={(y-top_y)/scale:5.2f}mm): NO YELLOW")
