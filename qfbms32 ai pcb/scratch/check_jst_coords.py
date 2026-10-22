import pcbnew

board = pcbnew.LoadBoard(r"c:\Users\quinn\Desktop\AI PCB CAD\Q VFBMS32 AI PCB\VFBMS32.kicad_pcb")

print("Connectors and ICs near X < 40:")
for fp in board.GetFootprints():
    ref = fp.GetReference()
    pos = fp.GetPosition()
    x = pcbnew.ToMM(pos.x)
    y = pcbnew.ToMM(pos.y)
    if x < 40:
        print(f"  {ref:12s} at ({x:6.2f}, {y:6.2f}) - {fp.GetFPID().GetLibItemName()}")
