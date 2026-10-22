import numpy as np

# In KiCad footprint:
# For XT30PW-F:
# Footprint is at (5.2, 7.45), rot=0.
# 3D model properties:
# offset = (0.8, 0.0, 0.0)
# rotate = (0.0, 0.0, 90.0)
# scale = (1.0, 1.0, 1.0)

# How KiCad transforms 3D model coordinates (Xm, Ym, Zm):
# 1. Scale
# 2. Rotation: rotate (Rx, Ry, Rz) in degrees
# For (0, 0, 90):
#   X' = -Ym
#   Y' = Xm
#   Z' = Zm
# 3. Offset (ox, oy, oz):
#   X_fp = X' + ox = -Ym + ox
#   Y_fp = Y' + oy = Xm + oy
#   Z_fp = Z' + oz = Zm + oz

# Let's check XT30PW-F:
# ox = 0.8, oy = 0, oz = 0.
# Ground tabs in STEP:
# Tab 1: Xm = -5.500, Ym = 2.942, Zm = -2.176
# Tab 2: Xm = +5.500, Ym = 2.942, Zm = -2.176
# Pins in STEP:
# Pin 1: Xm = -2.500, Ym = 7.942, Zm = -0.169 (or extends to Zm=-2.176)
# Pin 2: Xm = +2.500, Ym = 7.942, Zm = -0.169

# Transformed to Footprint coordinates:
# Tab 1:
#   X_fp = -2.942 + 0.8 = -2.142
#   Y_fp = -5.500
# Tab 2:
#   X_fp = -2.942 + 0.8 = -2.142
#   Y_fp = +5.500
# Pin 1:
#   X_fp = -7.942 + 0.8 = -7.142
#   Y_fp = -2.500
# Pin 2:
#   X_fp = -7.942 + 0.8 = -7.142
#   Y_fp = +2.500

print("XT30PW-F mapped to Footprint:")
print(f"  Tab 1 (Y=-5.5): X_fp = {-2.942 + 0.8:.3f}, Y_fp = -5.5")
print(f"  Tab 2 (Y=+5.5): X_fp = {-2.942 + 0.8:.3f}, Y_fp = +5.5")
print(f"  Pin 1 (Y=-2.5): X_fp = {-7.942 + 0.8:.3f}, Y_fp = -2.5")
print(f"  Pin 2 (Y=+2.5): X_fp = {-7.942 + 0.8:.3f}, Y_fp = +2.5")

# Now let's check board coordinates with FP at (5.2, 7.45):
# Board X = FP_X + X_fp
# Board Y = FP_Y + Y_fp
print("XT30PW-F mapped to Board (FP at 5.2, 7.45):")
print(f"  Tab 1: Board_X = {5.2 - 2.142:.3f}, Board_Y = {7.45 - 5.5:.3f} = 1.950")
print(f"  Tab 2: Board_X = {5.2 - 2.142:.3f}, Board_Y = {7.45 + 5.5:.3f} = 12.950")
print(f"  Pin 1: Board_X = {5.2 - 7.142:.3f}, Board_Y = {7.45 - 2.5:.3f} = 4.950")
print(f"  Pin 2: Board_X = {5.2 - 7.142:.3f}, Board_Y = {7.45 + 2.5:.3f} = 9.950")

