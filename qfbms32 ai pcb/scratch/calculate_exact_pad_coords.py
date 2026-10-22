import re
import numpy as np

# In KiCad top layer:
# (rotate (xyz 0 0 90)):
# x_rot = y_step
# y_rot = -x_step
# z_rot = z_step

def inspect_pins_and_tabs(name, step_path, fp_pos, offset):
    print(f"\n=================== {name} ===================")
    with open(step_path, "r", errors="ignore") as f:
        text = f.read()

    # Find all cylinder axes with their radius and centers
    # #axis_id = AXIS2_PLACEMENT_3D('NONE', #pt_id, #dir1, #dir2)
    # #cyl_id = CYLINDRICAL_SURFACE('NONE', #axis_id, radius)
    cyls = re.findall(r"CYLINDRICAL_SURFACE\s*\(\s*'[^']*'\s*,\s*#(\d+)\s*,\s*([-\d.eE]+)\s*\)", text)
    placements = {}
    for m in re.finditer(r"#(\d+)\s*=\s*AXIS2_PLACEMENT_3D\s*\(\s*'[^']*'\s*,\s*#(\d+)\s*,\s*#(\d+)", text):
        placements[m.group(1)] = (m.group(2), m.group(3))

    points = {}
    for m in re.finditer(r"#(\d+)\s*=\s*CARTESIAN_POINT\s*\(\s*'[^']*'\s*,\s*\(\s*([-\d.eE]+)\s*,\s*([-\d.eE]+)\s*,\s*([-\d.eE]+)\s*\)\s*\)", text):
        points[m.group(1)] = (float(m.group(2)), float(m.group(3)), float(m.group(4)))

    directions = {}
    for m in re.finditer(r"#(\d+)\s*=\s*DIRECTION\s*\(\s*'[^']*'\s*,\s*\(\s*([-\d.eE]+)\s*,\s*([-\d.eE]+)\s*,\s*([-\d.eE]+)\s*\)\s*\)", text):
        directions[m.group(1)] = (float(m.group(2)), float(m.group(3)), float(m.group(4)))

    # We want vertical cylinders (axis along Z, i.e. dir = (0, 0, 1) or (0, 0, -1))
    vertical_cyls = []
    for axis_id, rad_str in cyls:
        r = float(rad_str)
        if axis_id in placements:
            pt_id, dir_id = placements[axis_id]
            pt = points.get(pt_id)
            d = directions.get(dir_id)
            if pt and d and abs(d[2]) > 0.9:
                vertical_cyls.append((r, pt))

    # Transform to footprint coordinates and board coordinates:
    # x_fp = y_step + offset[0]
    # y_fp = -x_step + offset[1]
    # x_board = x_fp + fp_pos[0]
    # y_board = y_fp + fp_pos[1]
    
    unique_cyls = {}
    for r, pt in vertical_cyls:
        xs, ys, zs = pt
        xf = ys + offset[0]
        yf = -xs + offset[1]
        xb = xf + fp_pos[0]
        yb = yf + fp_pos[1]
        key = (round(xb, 2), round(yb, 2), round(r, 2))
        if key not in unique_cyls:
            unique_cyls[key] = (r, pt, (xf, yf), (xb, yb))

    for key, (r, pt, fp_c, brd_c) in sorted(unique_cyls.items(), key=lambda item: item[1][3][1]):
        print(f"Cylinder R={r:.3f} mm (diam {2*r:.3f} mm):")
        print(f"  STEP: ({pt[0]:.3f}, {pt[1]:.3f}, {pt[2]:.3f})")
        print(f"  FP coord: ({fp_c[0]:.3f}, {fp_c[1]:.3f})")
        print(f"  Board coord: ({brd_c[0]:.3f}, {brd_c[1]:.3f})")

inspect_pins_and_tabs("J_CHG1 (XT30PW-F)", r"3dmodels/XT30PW-F.step", (5.2, 7.45), (0.8, 0, 0))
inspect_pins_and_tabs("J_BAT1 (XT30PW-M)", r"3dmodels/XT30PW-M.step", (4.0, 24.55), (4.1, 0, 2.5))
