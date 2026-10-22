import re
import numpy as np

# In XT30PW-M.step:
with open(r"3dmodels/XT30PW-M.step", "r", errors="ignore") as f:
    text = f.read()

# Find PLANAR_BOX or PLANE or CARTESIAN_POINT
# In KiCad, rotation is (0, 0, 90).
# Let's inspect planes: #id = PLANE ( 'NONE', #axis_id ) ;
planes = re.findall(r"PLANE\s*\(\s*'[^']*'\s*,\s*#(\d+)\s*\)", text)
placements = {}
for m in re.finditer(r"#(\d+)\s*=\s*AXIS2_PLACEMENT_3D\s*\(\s*'[^']*'\s*,\s*#(\d+)\s*,\s*#(\d+)\s*,\s*#(\d+)", text):
    placements[m.group(1)] = (m.group(2), m.group(3), m.group(4))

directions = {}
for m in re.finditer(r"#(\d+)\s*=\s*DIRECTION\s*\(\s*'[^']*'\s*,\s*\(\s*([-\d.eE]+)\s*,\s*([-\d.eE]+)\s*,\s*([-\d.eE]+)\s*\)\s*\)", text):
    directions[m.group(1)] = (float(m.group(2)), float(m.group(3)), float(m.group(4)))

points = {}
for m in re.finditer(r"#(\d+)\s*=\s*CARTESIAN_POINT\s*\(\s*'[^']*'\s*,\s*\(\s*([-\d.eE]+)\s*,\s*([-\d.eE]+)\s*,\s*([-\d.eE]+)\s*\)\s*\)", text):
    points[m.group(1)] = (float(m.group(2)), float(m.group(3)), float(m.group(4)))

print(f"Total planes in XT30PW-M: {len(planes)}")
for p_axis in planes:
    if p_axis in placements:
        pt_id, norm_id, ref_id = placements[p_axis]
        pt = points.get(pt_id)
        norm = directions.get(norm_id)
        if pt and norm:
            # Check planes with normal along Z (horizontal planes)
            if abs(norm[2]) > 0.9:
                print(f"Horizontal plane at Z = {pt[2]:.4f}, normal = {norm}")

