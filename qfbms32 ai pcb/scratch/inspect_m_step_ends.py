import re
import numpy as np

with open(r"3dmodels/XT30PW-M.step", "r", errors="ignore") as f:
    text = f.read()

pts = re.findall(r"CARTESIAN_POINT\s*\(\s*'[^']*'\s*,\s*\(\s*([-\d.eE]+)\s*,\s*([-\d.eE]+)\s*,\s*([-\d.eE]+)\s*\)\s*\)", text)
pts = np.array([[float(p[0]), float(p[1]), float(p[2])] for p in pts])

print(f"XT30PW-M raw Y range: [{pts[:,1].min():.3f}, {pts[:,1].max():.3f}]")

# Let's check points near Y min (-9.0)
p_ymin = pts[pts[:, 1] < -8.0]
print(f"Points near Y min (-9.0): {len(p_ymin)}")
for p in p_ymin[:5]:
    print(f"  ({p[0]:.3f}, {p[1]:.3f}, {p[2]:.3f})")

# Let's check points near Y max (+4.95)
p_ymax = pts[pts[:, 1] > 4.0]
print(f"Points near Y max (+4.95): {len(p_ymax)}")
for p in p_ymax[:5]:
    print(f"  ({p[0]:.3f}, {p[1]:.3f}, {p[2]:.3f})")

# Where are the contact pins (gold)?
# Earlier we found:
# Radius 0.950 at (-2.5, -8.5, 0.0) and (+2.5, -8.5, 0.0)!
# And Radius 0.950 at (-2.5, 4.0, -5.0) and (+2.5, 4.0, -5.0)!
