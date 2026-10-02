import re
import numpy as np

def extract_cylinders_and_pins(path):
    print(f"\n================ {path} ================")
    with open(path, "r", errors="ignore") as f:
        text = f.read()

    # In STEP files, CYLINDRICAL_SURFACE has an AXIS2_PLACEMENT_3D with axis and radius.
    # e.g. #123 = CYLINDRICAL_SURFACE ( 'NONE', #456, 1.25 ) ;
    cyls = re.findall(r"CYLINDRICAL_SURFACE\s*\(\s*'[^']*'\s*,\s*#(\d+)\s*,\s*([-\d.eE]+)\s*\)", text)
    print(f"Total cylindrical surfaces found: {len(cyls)}")

    # Let's map placement IDs to CARTESIAN_POINT
    # #456 = AXIS2_PLACEMENT_3D ( 'NONE', #789, ... )
    placements = {}
    for m in re.finditer(r"#(\d+)\s*=\s*AXIS2_PLACEMENT_3D\s*\(\s*'[^']*'\s*,\s*#(\d+)", text):
        placements[m.group(1)] = m.group(2)

    points = {}
    for m in re.finditer(r"#(\d+)\s*=\s*CARTESIAN_POINT\s*\(\s*'[^']*'\s*,\s*\(\s*([-\d.eE]+)\s*,\s*([-\d.eE]+)\s*,\s*([-\d.eE]+)\s*\)\s*\)", text):
        points[m.group(1)] = (float(m.group(2)), float(m.group(3)), float(m.group(4)))

    cyl_info = []
    for axis_id, radius in cyls:
        r = float(radius)
        pt_id = placements.get(axis_id)
        if pt_id and pt_id in points:
            pt = points[pt_id]
            cyl_info.append((r, pt))

    # Print unique cylinders sorted by radius
    for r, pt in sorted(cyl_info, key=lambda x: (round(x[0], 2), round(x[1][0], 2), round(x[1][1], 2))):
        print(f"  Radius {r:.3f} mm (diam {2*r:.3f} mm) at origin ({pt[0]:.3f}, {pt[1]:.3f}, {pt[2]:.3f})")

extract_cylinders_and_pins(r"c:\Users\quinn\Desktop\AI PCB CAD\Q VFBMS32 AI PCB\3dmodels\XT30PW-F.step")
extract_cylinders_and_pins(r"c:\Users\quinn\Desktop\AI PCB CAD\Q VFBMS32 AI PCB\3dmodels\XT30PW-M.step")
