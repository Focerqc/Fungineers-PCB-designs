import re
import numpy as np

def analyze_step(path):
    with open(path, 'r', encoding='latin-1', errors='ignore') as f:
        content = f.read()

    pts = []
    # CARTESIAN_POINT ( 'NONE',  ( X, Y, Z ) )
    for m in re.finditer(r"CARTESIAN_POINT\s*\(\s*'[^']*'\s*,\s*\(\s*([-\d.E+]+)\s*,\s*([-\d.E+]+)\s*,\s*([-\d.E+]+)\s*\)\s*\)", content):
        x, y, z = float(m.group(1)), float(m.group(2)), float(m.group(3))
        pts.append((x, y, z))
    pts = np.array(pts)
    print(f"File: {path}")
    print(f"Total points: {len(pts)}")
    print(f"X range: [{pts[:,0].min():.4f}, {pts[:,0].max():.4f}] (span: {np.ptp(pts[:,0]):.4f})")
    print(f"Y range: [{pts[:,1].min():.4f}, {pts[:,1].max():.4f}] (span: {np.ptp(pts[:,1]):.4f})")
    print(f"Z range: [{pts[:,2].min():.4f}, {pts[:,2].max():.4f}] (span: {np.ptp(pts[:,2]):.4f})")

    # When rotated by (0, 0, 90 deg):
    # In KiCad rotation (Euler angles around Z, then Y, then X, or standard Z rotation):
    # For a point (x, y, z), rotating +90 deg around Z:
    # x' = -y
    # y' = x
    # z' = z
    # Let's check how KiCad rotates 3D models with (rotate (xyz 0 0 90)):
    # x_rot = -y, y_rot = x, z_rot = z
    # Then offset (ox, oy, oz):
    # final_x = x_rot + ox
    return pts

f_pts = analyze_step(r"c:\Users\quinn\Desktop\AI PCB CAD\Q VFBMS32 AI PCB\3dmodels\XT30PW-F.step")
m_pts = analyze_step(r"c:\Users\quinn\Desktop\AI PCB CAD\Q VFBMS32 AI PCB\3dmodels\XT30PW-M.step")
