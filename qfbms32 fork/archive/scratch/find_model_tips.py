import re
import numpy as np

def analyze_model_tips(step_file, rot_deg, offset, fp_pos):
    with open(step_file, "r", errors="ignore") as f:
        text = f.read()
    
    pts = re.findall(r"CARTESIAN_POINT\s*\(\s*'[^']*'\s*,\s*\(\s*([-\d.eE]+)\s*,\s*([-\d.eE]+)\s*,\s*([-\d.eE]+)\s*\)\s*\)", text)
    arr = np.array([[float(p[0]), float(p[1]), float(p[2])] for p in pts])
    
    # KiCad 3D rotation:
    # If rot is (0, 0, 90):
    rad = np.radians(rot_deg[2])
    # KiCad rotates counterclockwise around Z:
    # X' = X*cos(th) - Y*sin(th)
    # Y' = X*sin(th) + Y*cos(th)
    # For th = 90 deg: cos=0, sin=1 => X' = -Y, Y' = X, Z' = Z
    x_rot = arr[:, 0]*np.cos(rad) - arr[:, 1]*np.sin(rad)
    y_rot = arr[:, 0]*np.sin(rad) + arr[:, 1]*np.cos(rad)
    z_rot = arr[:, 2]
    
    # Add offset
    x_fp = x_rot + offset[0]
    y_fp = y_rot + offset[1]
    z_fp = z_rot + offset[2]
    
    # Add board position
    x_board = x_fp + fp_pos[0]
    y_board = y_fp + fp_pos[1]
    
    print(f"\n--- {step_file} ---")
    print(f"FP pos: {fp_pos}, offset: {offset}, rot: {rot_deg}")
    print(f"Board X range: [{x_board.min():.3f}, {x_board.max():.3f}]")
    print(f"Board Y range: [{y_board.min():.3f}, {y_board.max():.3f}]")
    print(f"Z range: [{z_fp.min():.3f}, {z_fp.max():.3f}]")
    
    # Find points near bottom (lowest Z):
    low_z = z_fp.min()
    print(f"Lowest Z is {low_z:.3f} mm")
    bottom_pts = np.column_stack((x_board, y_board, z_fp))[z_fp < low_z + 1.0]
    # Cluster bottom points
    print(f"Number of points near bottom Z (< {low_z+1.0:.3f}): {len(bottom_pts)}")
    # Find local clusters of bottom points
    for p in bottom_pts[::max(1, len(bottom_pts)//15)]:
        print(f"  Tip point: Board X={p[0]:.3f}, Board Y={p[1]:.3f}, Z={p[2]:.3f}")

analyze_model_tips(r"3dmodels/XT30PW-F.step", (0, 0, 90), (0.8, 0.0, 0.0), (5.2, 7.45))
analyze_model_tips(r"3dmodels/XT30PW-M.step", (0, 0, 90), (4.1, 0.0, 0.0), (4.0, 24.55))
