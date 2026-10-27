import pcbnew

board = pcbnew.LoadBoard('qfbms32.kicad_pcb')
q2 = board.FindFootprintByReference("Q2")
if q2:
    print(f"Q2 pos: ({pcbnew.ToMM(q2.GetPosition().x):.2f}, {pcbnew.ToMM(q2.GetPosition().y):.2f}) rot={q2.GetOrientationDegrees()}")
    for pad in q2.Pads():
        pos = pad.GetPosition()
        print(f"  Pad {pad.GetName()}: ({pcbnew.ToMM(pos.x):.2f}, {pcbnew.ToMM(pos.y):.2f}) size=({pcbnew.ToMM(pad.GetSizeX()):.2f}, {pcbnew.ToMM(pad.GetSizeY()):.2f})")
