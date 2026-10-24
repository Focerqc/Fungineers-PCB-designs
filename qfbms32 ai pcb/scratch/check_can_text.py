import pcbnew

board = pcbnew.LoadBoard('qfbms32.kicad_pcb')
for t in board.GetDrawings():
    if isinstance(t, pcbnew.PCB_TEXT) and any(k in t.GetText() for k in ["CANH", "CANL", "ISO", "5V"]):
        pos = t.GetPosition()
        print(f"Text '{t.GetText()}' at ({pcbnew.ToMM(pos.x):.2f}, {pcbnew.ToMM(pos.y):.2f}) layer={board.GetLayerName(t.GetLayer())}")
