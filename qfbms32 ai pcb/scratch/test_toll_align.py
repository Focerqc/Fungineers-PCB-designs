import re
import numpy as np

# Footprint pads in TOLL-8_AGM15T03LL.kicad_mod:
# pad "D" at (0, -1.6), size 9.2 x 6.8
# pad 1..8 at (-4.2 to +4.2, 4.65)
# Footprint center (0, 0)
# Overall package body: 9.9 wide (along X: -4.95 to +4.95), 11.68 long (along Y: -5.84 to +5.84)
# Note that in footprint:
# Drain tab center Y = -1.6
# Pins center Y = +4.65
# Body center = (0, 0)

# STEP model:
step_path = r"c:\Users\quinn\Desktop\AI PCB CAD\Q VFBMS32 AI PCB\3dmodels\TOLL-8.step"
text = open(step_path, errors='ignore').read()
pts = re.findall(r'CARTESIAN_POINT\s*\(\s*\'[^\']*\'\s*,\s*\(\s*([-\d.eE]+)\s*,\s*([-\d.eE]+)\s*,\s*([-\d.eE]+)\s*\)\s*\)', text)
pts = [tuple(map(float, p)) for p in pts]

xs = [p[0] for p in pts]
ys = [p[1] for p in pts]
zs = [p[2] for p in pts]

cx_step = (min(xs) + max(xs)) / 2.0
cy_step = (min(ys) + max(ys)) / 2.0
print(f"STEP bounds: X [{min(xs):.3f}, {max(xs):.3f}] (mid {cx_step:.3f}), Y [{min(ys):.3f}, {max(ys):.3f}] (mid {cy_step:.3f}), Z [{min(zs):.3f}, {max(zs):.3f}]")

# Earlier we found:
# In STEP model:
# X has drain at positive X (+5.89) and pins at negative X (-5.79)
# Y has width -4.95 to +4.95 (symmetric around 0)
# In footprint:
# Y has drain at negative Y and pins at positive Y
# X has width -4.95 to +4.95 (symmetric around 0)

# If we rotate STEP by (0, 0, -90):
# X_rot = Y_step
# Y_rot = -X_step
# Then pins (X_step < 0) will have Y_rot > 0 (matching footprint positive Y!)
# Drain (X_step > 0) will have Y_rot < 0 (matching footprint negative Y!)
# Width (Y_step) will become X_rot!
# Mid X_step is: ( -5.79 + 6.09 ) / 2 = +0.15
# So Y_rot center would be -0.15!
# Footprint body center is Y=0.
# So offset Y might be around -0.15 or 0.0.

print("Testing rotation (0, 0, -90):")
rot_pts = [(p[1], -p[0], p[2]) for p in pts]
rx = [p[0] for p in rot_pts]
ry = [p[1] for p in rot_pts]
rz = [p[2] for p in rot_pts]
print(f"Rotated bounds: X [{min(rx):.3f}, {max(rx):.3f}], Y [{min(ry):.3f}, {max(ry):.3f}], Z [{min(rz):.3f}, {max(rz):.3f}]")
