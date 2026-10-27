import pcbnew

board = pcbnew.LoadBoard('qfbms32.kicad_pcb')
for t in board.GetDrawings():
    if isinstance(t, pcbnew.PCB_TEXT):
        pos = t.GetPosition()
        x, y = pcbnew.ToMM(pos.x), pcbnew.ToMM(pos.y)
        if abs(x - 15.1) < 10 and abs(y - 1.13) < 10:
            print(f"Text: '{t.GetText()}' at ({x:.2f}, {y:.2f}) layer={board.GetLayerName(t.GetLayer())}")
