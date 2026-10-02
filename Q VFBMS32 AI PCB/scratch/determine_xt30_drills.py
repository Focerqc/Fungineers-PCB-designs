import pcbnew

# Footprint positions currently:
# J_CHG1 (Female): FP at (5.2, 7.45)
# J_BAT1 (Male): FP at (4.0, 24.55)

# Wait! The user says:
# "Keep XT30s Left-Aligned & Shift MOSFETs Right:
# Both XT30 connectors must remain flush with the left board edge (X = 0 mm mating boundary). Do not move them inward.
# Shift the Q1 and Q2 TOLL-8 MOSFETs to the right to provide proper clearance away from the XT30 terminal pins and mounting hardware.
# Maintain the heavy copper pours on F.Cu and B.Cu to connect the XT30 through-hole pins to the shifted drain tabs of the MOSFETs."

# Let's verify where the mating boundary of the connectors is relative to the footprint position:
# In VFBMS32_layout_top_hi_raw.png and test_exact.py:
# J_CHG1 was at (5.2, 7.45) with 3D model offset (0.8, 0, 0), rot (0, 0, 90).
# J_BAT1 was at (4.0, 24.55) with 3D model offset (4.1, 0, 0), rot (0, 0, 90).
# Let's check where the left edge (mating face) of the connectors is in board X coordinates!

import re, numpy as np

def get_model_bounds(step_path, offset, rot_deg, fp_pos):
    with open(step_path, "r", errors="ignore") as f:
        text = f.read()
    pts = re.findall(r"CARTESIAN_POINT\s*\(\s*'[^']*'\s*,\s*\(\s*([-\d.eE]+)\s*,\s*([-\d.eE]+)\s*,\s*([-\d.eE]+)\s*\)\s*\)", text)
    arr = np.array([[float(p[0]), float(p[1]), float(p[2])] for p in pts])
    
    # rotate (0, 0, 90): X' = -Y, Y' = X, Z' = Z
    rad = np.radians(rot_deg[2])
    x_rot = arr[:, 0]*np.cos(rad) - arr[:, 1]*np.sin(rad)
    y_rot = arr[:, 0]*np.sin(rad) + arr[:, 1]*np.cos(rad)
    z_rot = arr[:, 2]
    
    # offset + fp_pos
    x_board = x_rot + offset[0] + fp_pos[0]
    y_board = y_rot + offset[1] + fp_pos[1]
    z_board = z_rot + offset[2]
    
    return x_board, y_board, z_board, arr

print("--- XT30PW-F (Female) ---")
xf, yf, zf, raw_f = get_model_bounds(r"3dmodels/XT30PW-F.step", (0.8, 0, 0), (0, 0, 90), (5.2, 7.45))
print(f"Board X range: [{xf.min():.3f}, {xf.max():.3f}]")
print(f"Board Y range: [{yf.min():.3f}, {yf.max():.3f}]")
print(f"Board Z range: [{zf.min():.3f}, {zf.max():.3f}]")

print("\n--- XT30PW-M (Male) with Z_offset=2.5 ---")
xm, ym, zm, raw_m = get_model_bounds(r"3dmodels/XT30PW-M.step", (4.1, 0, 2.5), (0, 0, 90), (4.0, 24.55))
print(f"Board X range: [{xm.min():.3f}, {xm.max():.3f}]")
print(f"Board Y range: [{ym.min():.3f}, {ym.max():.3f}]")
print(f"Board Z range: [{zm.min():.3f}, {zm.max():.3f}]")

