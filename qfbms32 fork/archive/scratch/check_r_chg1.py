import pcbnew

board = pcbnew.LoadBoard('qfbms32.kicad_pcb')
fp = board.FindFootprintByReference('R_CHG1')
if fp:
    pos = fp.GetPosition()
    print("R_CHG1 pos:", pcbnew.ToMM(pos.x), pcbnew.ToMM(pos.y))
    print("R_CHG1 val:", fp.GetValue())
    print("R_CHG1 fp:", fp.GetFPID().GetLibItemName())
