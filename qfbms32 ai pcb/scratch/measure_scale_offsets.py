from PIL import Image

im = Image.open(r'c:\Users\quinn\Desktop\AI PCB CAD\raw_left_crop.png')
w, h = im.size

# Let's find the exact board edge (X=0.0 in board coordinates)
# Board is 32mm high in Y.
# Let's find top and bottom edge of board:
# In the middle (x=100)
top_y = None
bot_y = None
for y in range(h):
    r, g, b, a = im.getpixel((100, y))
    if a > 100:
        if top_y is None:
            top_y = y
        bot_y = y

board_pixel_height = bot_y - top_y
scale = board_pixel_height / 32.0  # pixels per mm
print(f"Top Y: {top_y}, Bottom Y: {bot_y}, Board height in pixels: {board_pixel_height}")
print(f"Scale: {scale:.3f} pixels/mm")

# Let's find the PCB left edge at Y=180 (middle)
pcb_left_x = None
for x in range(w):
    r, g, b, a = im.getpixel((x, 180))
    if a > 100 and (r < 100 and g > 50): # PCB green
        pcb_left_x = x
        break

print(f"PCB left edge at Y=180: x={pcb_left_x}")

# Let's find exact left edge of female connector at its center Y:
# Female connector center Y is around top_y + 5.8 * scale
f_y = int(top_y + 5.8 * scale)
f_left_x = None
for x in range(w):
    r, g, b, a = im.getpixel((x, f_y))
    if a > 100 and (r > 150 and g > 150): # yellow
        f_left_x = x
        break

# Let's find exact left edge of male connector at its center Y:
m_y = int(top_y + 26.2 * scale)
m_left_x = None
for x in range(w):
    r, g, b, a = im.getpixel((x, m_y))
    if a > 100 and (r > 150 and g > 150): # yellow
        m_left_x = x
        break

print(f"Female center y={f_y}: left yellow x={f_left_x}, diff from PCB edge = {f_left_x - pcb_left_x} px ({(f_left_x - pcb_left_x)/scale:.3f} mm)")
print(f"Male center y={m_y}: left yellow x={m_left_x}, diff from PCB edge = {m_left_x - pcb_left_x} px ({(m_left_x - pcb_left_x)/scale:.3f} mm)")
