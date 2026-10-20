from PIL import Image

img = Image.open('Q VFBMS32 AI PCB/_reference/vfbms32_cad_top_reference_rotated.png')
# Let's find exact centers of:
# 1003 resistor
# Diode 1
# Diode 2
# Diode 3
# Tan cap

# Let's inspect columns in the crop
scale_x = 130.0 / 813.0
scale_y = 32.0 / 200.0

# In cad_box_crop:
# We know the crop was taken at x=[-2, 53], y=[77, 119]
# Let's analyze pixel coordinates within this crop:
# Let's save an annotated version with pixel grid or coordinates marked

# Resistor: around x = 5-11 px -> center ~ 8 px -> 8 * 0.1599 = 1.28 mm
# Diode 1: around x = 16-24 px -> center ~ 20 px -> 20 * 0.1599 = 3.20 mm
# Diode 2: around x = 27-35 px -> center ~ 31 px -> 31 * 0.1599 = 4.96 mm
# Diode 3: around x = 38-46 px -> center ~ 42 px -> 42 * 0.1599 = 6.72 mm
# Capacitor: around x = 49-62 px -> center ~ 55 px -> 55 * 0.1599 = 8.79 mm (PCB had 8.2)

# Y center:
# The diode pads span y from ~82 to 115 px -> center ~ 98.5 px -> 98.5 * 0.16 = 15.76 mm!

print(f"Resistor: X = {8 * scale_x:.2f} mm, Y = {98.5 * scale_y:.2f} mm")
print(f"Diode 1:  X = {20 * scale_x:.2f} mm, Y = {98.5 * scale_y:.2f} mm")
print(f"Diode 2:  X = {31 * scale_x:.2f} mm, Y = {98.5 * scale_y:.2f} mm")
print(f"Diode 3:  X = {42 * scale_x:.2f} mm, Y = {98.5 * scale_y:.2f} mm")
