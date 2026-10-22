import re
import numpy as np

with open(r"3dmodels/XT30PW-F.step", "r", errors="ignore") as f:
    text = f.read()

# Let's inspect the bounding box of yellow plastic vs gold pins vs silver tabs
# Find STYLED_ITEM linking to COLOUR_RGB
# We saw colors:
# yellow: ('', '0.800000011920929', '0.760330617427826', '0.')
# gold: ('', '0.800000011920929', '0.666434764862061', '0.319999992847443')
# silver: ('', '0.699999988079071', '0.699999988079071', '0.699999988079071')

# Let's find ADVANCED_FACE items and their surfaces/bounds
pts = re.findall(r"CARTESIAN_POINT\s*\(\s*'[^']*'\s*,\s*\(\s*([-\d.eE]+)\s*,\s*([-\d.eE]+)\s*,\s*([-\d.eE]+)\s*\)\s*\)", text)
pts = np.array([[float(p[0]), float(p[1]), float(p[2])] for p in pts])

print("Raw points count:", len(pts))
print(f"X: [{pts[:,0].min():.3f}, {pts[:,0].max():.3f}]")
print(f"Y: [{pts[:,1].min():.3f}, {pts[:,1].max():.3f}]")
print(f"Z: [{pts[:,2].min():.3f}, {pts[:,2].max():.3f}]")

# Let's find which points have Z < -1 (bottom)
bot = pts[pts[:, 2] < -1.0]
print("Points with Z < -1:")
for p in bot:
    print(f"  ({p[0]:.3f}, {p[1]:.3f}, {p[2]:.3f})")
