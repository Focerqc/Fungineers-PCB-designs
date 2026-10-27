import re

def check_step_planes(path):
    with open(path, "r", errors="ignore") as f:
        text = f.read()

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

    print(f"\nHorizontal planes in {path}:")
    for p_axis in planes:
        if p_axis in placements:
            pt_id, norm_id, ref_id = placements[p_axis]
            pt = points.get(pt_id)
            norm = directions.get(norm_id)
            if pt and norm and abs(norm[2]) > 0.9:
                print(f"  Z = {pt[2]:.4f}, normal = {norm}")

check_step_planes(r"3dmodels/XT30PW-F.step")
check_step_planes(r"3dmodels/XT30PW-M.step")
