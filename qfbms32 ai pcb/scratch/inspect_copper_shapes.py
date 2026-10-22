import pcbnew

board = pcbnew.LoadBoard(r"c:\Users\quinn\Desktop\AI PCB CAD\Q VFBMS32 AI PCB\VFBMS32.kicad_pcb")

shapes = [d for d in board.GetDrawings() if isinstance(d, pcbnew.PCB_SHAPE) and d.GetLayer() in [pcbnew.F_Cu, pcbnew.B_Cu]]
tracks = [t for t in board.GetTracks() if not isinstance(t, pcbnew.PCB_VIA) and t.GetWidth() >= pcbnew.FromMM(2.0)]

print(f"Copper shapes on F.Cu/B.Cu: {len(shapes)}")
for i, s in enumerate(shapes):
    layer = board.GetLayerName(s.GetLayer())
    bb = s.GetBoundingBox()
    x0, y0 = pcbnew.ToMM(bb.GetX()), pcbnew.ToMM(bb.GetY())
    w, h = pcbnew.ToMM(bb.GetWidth()), pcbnew.ToMM(bb.GetHeight())
    print(f"  Shape {i}: Layer={layer}, Box=({x0:.2f}, {y0:.2f}, w={w:.2f}, h={h:.2f})")

print(f"\nHeavy tracks: {len(tracks)}")
for i, t in enumerate(tracks):
    layer = board.GetLayerName(t.GetLayer())
    w = pcbnew.ToMM(t.GetWidth())
    sp = t.GetStart()
    ep = t.GetEnd()
    print(f"  Track {i}: Layer={layer}, w={w:.2f}, from ({pcbnew.ToMM(sp.x):.2f}, {pcbnew.ToMM(sp.y):.2f}) to ({pcbnew.ToMM(ep.x):.2f}, {pcbnew.ToMM(ep.y):.2f})")
