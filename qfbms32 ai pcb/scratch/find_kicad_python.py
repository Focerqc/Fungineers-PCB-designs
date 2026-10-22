import os

kicad_root = r"C:\Program Files\KiCad\10.0"
found = []
for root, dirs, files in os.walk(kicad_root):
    for f in files:
        if "pcbnew" in f.lower() or "python" in f.lower():
            p = os.path.join(root, f)
            found.append(p)

for p in sorted(found):
    print(p)
