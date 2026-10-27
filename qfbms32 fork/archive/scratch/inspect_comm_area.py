import pcbnew

board = pcbnew.LoadBoard('qfbms32.kicad_pcb')

print("=== Pads near (30.8, 28.0) ===")
for fp in board.GetFootprints():
    for pad in fp.Pads():
        pos = pad.GetPosition()
        x = pcbnew.ToMM(pos.x)
        y = pcbnew.ToMM(pos.y)
        if abs(x - 30.8) < 6 and abs(y - 28.0) < 6:
            print(f"Pad: {fp.GetReference()} {pad.GetName()} at ({x:.2f}, {y:.2f}) net={pad.GetNetname()}")

print("=== Tracks near (30.8, 28.0) ===")
for track in board.GetTracks():
    start = track.GetStart()
    end = track.GetEnd()
    sx, sy = pcbnew.ToMM(start.x), pcbnew.ToMM(start.y)
    ex, ey = pcbnew.ToMM(end.x), pcbnew.ToMM(end.y)
    if (abs(sx - 30.8) < 4 and abs(sy - 28.0) < 4) or (abs(ex - 30.8) < 4 and abs(ey - 28.0) < 4):
        print(f"Track: ({sx:.2f}, {sy:.2f}) -> ({ex:.2f}, {ey:.2f}) net={track.GetNetname()}")

print("=== PCB Shapes near (30.8, 28.0) ===")
for d in board.GetDrawings():
    if isinstance(d, pcbnew.PCB_SHAPE):
        bbox = d.GetBoundingBox()
        bx, by = pcbnew.ToMM(bbox.GetX()), pcbnew.ToMM(bbox.GetY())
        bw, bh = pcbnew.ToMM(bbox.GetWidth()), pcbnew.ToMM(bbox.GetHeight())
        if abs(bx - 30.8) < 8 and abs(by - 28.0) < 8:
            print(f"Shape: layer={board.GetLayerName(d.GetLayer())} bbox=({bx:.2f}, {by:.2f}, {bw:.2f}, {bh:.2f})")
