import pcbnew

board = pcbnew.LoadBoard(r"c:\Users\quinn\Desktop\AI PCB CAD\Q VFBMS32 AI PCB\VFBMS32.kicad_pcb")

zones = board.Zones()
print(f"Total zones on board: {len(zones)}")

for i, z in enumerate(zones):
    net_name = z.GetNetname()
    layer = board.GetLayerName(z.GetLayer())
    poly = z.GetFilledPolysList()
    outline = z.Outline()
    pts_count = outline.PointCount() if outline else 0
    box = z.GetBoundingBox()
    x0, y0 = pcbnew.ToMM(box.GetX()), pcbnew.ToMM(box.GetY())
    w, h = pcbnew.ToMM(box.GetWidth()), pcbnew.ToMM(box.GetHeight())
    print(f"Zone {i}: Net='{net_name}', Layer='{layer}', Box=({x0:.1f}, {y0:.1f}, w={w:.1f}, h={h:.1f}), Points={pts_count}")

