import re

def inspect_features(path):
    print(f"=== {path} ===")
    with open(path, 'r', encoding='latin-1', errors='ignore') as f:
        lines = f.readlines()
    
    # Find cylindrical surfaces / circles or extreme points
    pts = []
    for line in lines:
        m = re.search(r"CARTESIAN_POINT\s*\(\s*'[^']*'\s*,\s*\(\s*([-\d.E+]+)\s*,\s*([-\d.E+]+)\s*,\s*([-\d.E+]+)\s*\)\s*\)", line)
        if m:
            pts.append((float(m.group(1)), float(m.group(2)), float(m.group(3))))

    # Let's sort by Y to see what is at min Y and max Y
    pts_by_y = sorted(pts, key=lambda p: p[1])
    print("Min Y points (first 5):")
    for p in pts_by_y[:5]:
        print(f"  ({p[0]:.4f}, {p[1]:.4f}, {p[2]:.4f})")
    print("Max Y points (last 5):")
    for p in pts_by_y[-5:]:
        print(f"  ({p[0]:.4f}, {p[1]:.4f}, {p[2]:.4f})")

inspect_features(r"c:\Users\quinn\Desktop\AI PCB CAD\Q VFBMS32 AI PCB\3dmodels\XT30PW-F.step")
inspect_features(r"c:\Users\quinn\Desktop\AI PCB CAD\Q VFBMS32 AI PCB\3dmodels\XT30PW-M.step")
