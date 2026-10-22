import os
import re

def analyze_step(path):
    print("=== Analyzing", path, "===")
    with open(path, "r", errors="ignore") as f:
        text = f.read()
    
    # find CARTESIAN_POINT
    pts = re.findall(r"CARTESIAN_POINT\s*\(\s*'[^\']*'\s*,\s*\(\s*([-\d.eE]+)\s*,\s*([-\d.eE]+)\s*,\s*([-\d.eE]+)\s*\)\s*\)", text)
    if pts:
        xs = [float(p[0]) for p in pts]
        ys = [float(p[1]) for p in pts]
        zs = [float(p[2]) for p in pts]
        print(f"  Points: {len(pts)}")
        print(f"  X range: {min(xs):.3f} to {max(xs):.3f} (size {max(xs)-min(xs):.3f})")
        print(f"  Y range: {min(ys):.3f} to {max(ys):.3f} (size {max(ys)-min(ys):.3f})")
        print(f"  Z range: {min(zs):.3f} to {max(zs):.3f} (size {max(zs)-min(zs):.3f})")

analyze_step(r"c:\Users\quinn\Desktop\AI PCB CAD\Q VFBMS32 AI PCB\3dmodels\XT30PW-F.step")
analyze_step(r"c:\Users\quinn\Desktop\AI PCB CAD\Q VFBMS32 AI PCB\3dmodels\XT30PW-M.step")
