import re

step_path = r"C:\Program Files\KiCad\10.0\share\kicad\3dmodels\Package_TO_SOT_SMD.3dshapes\Infineon_PG-HSOF-8-1.step"
with open(step_path, 'r', errors='ignore') as f:
    text = f.read()

# Let's inspect the bottom surface pads (Z near 0)
pts = re.findall(r'CARTESIAN_POINT\s*\(\s*\'[^\']*\'\s*,\s*\(\s*([-\d.eE]+)\s*,\s*([-\d.eE]+)\s*,\s*([-\d.eE]+)\s*\)\s*\)', text)
bottom_pts = []
for p in pts:
    x, y, z = float(p[0]), float(p[1]), float(p[2])
    if abs(z) < 0.05:
        bottom_pts.append((x, y, z))

print(f'Found {len(bottom_pts)} points on bottom contact plane (Z=0)')
# Let's check X and Y range of bottom points
xs = [p[0] for p in bottom_pts]
ys = [p[1] for p in bottom_pts]
print(f'Bottom plane X range: {min(xs):.2f} to {max(xs):.2f}')
print(f'Bottom plane Y range: {min(ys):.2f} to {max(ys):.2f}')

# Let's find where the 8 small leads are vs the large drain tab
# In TOLL, the 8 small leads are at one end along the length, and the large drain pad covers most of the other end
neg_x_pts = [p for p in bottom_pts if p[0] < -1.0]
pos_x_pts = [p for p in bottom_pts if p[0] > 1.0]
print(f'Points with X < -1.0: {len(neg_x_pts)}, Y range: {min([p[1] for p in neg_x_pts]):.2f} to {max([p[1] for p in neg_x_pts]):.2f}')
print(f'Points with X > 1.0: {len(pos_x_pts)}, Y range: {min([p[1] for p in pos_x_pts]):.2f} to {max([p[1] for p in pos_x_pts]):.2f}')
