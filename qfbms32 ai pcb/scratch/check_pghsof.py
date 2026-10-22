import re

step_path = r"C:\Program Files\KiCad\10.0\share\kicad\3dmodels\Package_TO_SOT_SMD.3dshapes\Infineon_PG-HSOF-8-1.step"
with open(step_path, 'r', errors='ignore') as f:
    text = f.read()

pts = re.findall(r'CARTESIAN_POINT\s*\(\s*\'[^\']*\'\s*,\s*\(\s*([-\d.eE]+)\s*,\s*([-\d.eE]+)\s*,\s*([-\d.eE]+)\s*\)\s*\)', text)
xs = [float(p[0]) for p in pts]
ys = [float(p[1]) for p in pts]
zs = [float(p[2]) for p in pts]
print('Infineon_PG-HSOF-8-1 STEP bounds:')
print(f'X: min={min(xs):.2f}, max={max(xs):.2f}, span={max(xs)-min(xs):.2f}')
print(f'Y: min={min(ys):.2f}, max={max(ys):.2f}, span={max(ys)-min(ys):.2f}')
print(f'Z: min={min(zs):.2f}, max={max(zs):.2f}, span={max(zs)-min(zs):.2f}')
