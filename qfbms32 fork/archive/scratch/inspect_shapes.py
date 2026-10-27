import pcbnew

board = pcbnew.LoadBoard('qfbms32.kicad_pcb')
for d in board.GetDrawings():
    if isinstance(d, pcbnew.PCB_SHAPE):
        layer = board.GetLayerName(d.GetLayer())
        bbox = d.GetBoundingBox()
        bx = pcbnew.ToMM(bbox.GetX())
        by = pcbnew.ToMM(bbox.GetY())
        bw = pcbnew.ToMM(bbox.GetWidth())
        bh = pcbnew.ToMM(bbox.GetHeight())
        start = d.GetStart()
        end = d.GetEnd()
        sx, sy = pcbnew.ToMM(start.x), pcbnew.ToMM(start.y)
        ex, ey = pcbnew.ToMM(end.x), pcbnew.ToMM(end.y)
        print(f"Shape: layer={layer} type={d.GetShapeStr()} start=({sx:.2f}, {sy:.2f}) end=({ex:.2f}, {ey:.2f}) bbox=({bx:.2f}, {by:.2f}, {bw:.2f}, {bh:.2f})")
