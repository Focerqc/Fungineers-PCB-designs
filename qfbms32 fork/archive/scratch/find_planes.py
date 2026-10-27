import re

def find_y_planes(path):
    print(f"=== {path} ===")
    with open(path, 'r', encoding='latin-1', errors='ignore') as f:
        content = f.read()

    # Look for PLANE with normal (0, 1, 0) or (0, -1, 0)
    # PLANE ( '', #axis2_placement_3d )
    # AXIS2_PLACEMENT_3D ( '', #point, #axis, #ref )
    pts = {}
    for m in re.finditer(r"#(\d+)\s*=\s*CARTESIAN_POINT\s*\(\s*'[^']*'\s*,\s*\(\s*([-\d.E+]+)\s*,\s*([-\d.E+]+)\s*,\s*([-\d.E+]+)\s*\)\s*\)", content):
        pts[m.group(1)] = (float(m.group(2)), float(m.group(3)), float(m.group(4)))

    dirs = {}
    for m in re.finditer(r"#(\d+)\s*=\s*DIRECTION\s*\(\s*'[^']*'\s*,\s*\(\s*([-\d.E+]+)\s*,\s*([-\d.E+]+)\s*,\s*([-\d.E+]+)\s*\)\s*\)", content):
        dirs[m.group(1)] = (float(m.group(2)), float(m.group(3)), float(m.group(4)))

    placements = {}
    for m in re.finditer(r"#(\d+)\s*=\s*AXIS2_PLACEMENT_3D\s*\(\s*'[^']*'\s*,\s*#(\d+)\s*,\s*#(\d+)\s*,\s*#(\d+)\s*\)", content):
        placements[m.group(1)] = (m.group(2), m.group(3), m.group(4))

    for m in re.finditer(r"#(\d+)\s*=\s*PLANE\s*\(\s*'[^']*'\s*,\s*#(\d+)\s*\)", content):
        pl_id = m.group(2)
        if pl_id in placements:
            pt_id, ax_id, ref_id = placements[pl_id]
            normal = dirs.get(ax_id, (0,0,0))
            # Check if normal is along Y (i.e. abs(normal[1]) > 0.99)
            if abs(normal[1]) > 0.99:
                pt = pts.get(pt_id, (0,0,0))
                print(f"Plane normal {normal} at Y = {pt[1]:.4f} (origin: {pt})")

find_y_planes(r"c:\Users\quinn\Desktop\AI PCB CAD\Q VFBMS32 AI PCB\3dmodels\XT30PW-F.step")
find_y_planes(r"c:\Users\quinn\Desktop\AI PCB CAD\Q VFBMS32 AI PCB\3dmodels\XT30PW-M.step")
