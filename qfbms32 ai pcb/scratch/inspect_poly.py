import pcbnew

board = pcbnew.LoadBoard('qfbms32.kicad_pcb')
for d in board.GetDrawings():
    if isinstance(d, pcbnew.PCB_SHAPE) and board.GetLayerName(d.GetLayer()) == "F.Cu":
        poly = d.GetPolyShape()
        print("Poly outlines count:", poly.OutlineCount())
        for o in range(poly.OutlineCount()):
            outline = poly.Outline(o)
            pts = [(pcbnew.ToMM(outline.CPoint(p).x), pcbnew.ToMM(outline.CPoint(p).y)) for p in range(outline.PointCount())]
            print(f"Outline {o}: {pts}")
