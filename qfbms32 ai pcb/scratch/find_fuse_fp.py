import os

fuse_lib = r"C:\Program Files\KiCad\10.0\share\kicad\footprints\Fuse.pretty"
if os.path.exists(fuse_lib):
    fps = [f for f in os.listdir(fuse_lib) if f.endswith('.kicad_mod')]
    for f in sorted(fps):
        if any(k in f for k in ['2410', '6125', 'SMD', '1808', '1206', 'Littelfuse', 'Fuse']):
            print(f)
