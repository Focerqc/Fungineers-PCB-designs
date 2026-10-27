import pcbnew

board = pcbnew.LoadBoard('qfbms32.kicad_pcb')
for t in board.GetDrawings():
    if isinstance(t, pcbnew.PCB_TEXT) and board.GetLayerName(t.GetLayer()) == "F.Silkscreen":
        pos = t.GetPosition()
        x, y = pcbnew.ToMM(pos.x), pcbnew.ToMM(pos.y)
        print(f"F.SilkS Text: '{t.GetText()}' at ({x:.2f}, {y:.2f})")
