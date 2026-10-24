import pcbnew

board = pcbnew.LoadBoard("qfbms32 ai pcb/qfbms32.kicad_pcb")

for fp in board.GetFootprints():
    pos = fp.GetPosition()
    x, y = pcbnew.ToMM(pos.x), pcbnew.ToMM(pos.y)
    if abs(x - 30.78) < 1.0 and abs(y - 29.83) < 1.0:
        print(f"Ref: {fp.GetReference()} Val: {fp.GetValue()} FP: {fp.GetFPID().GetLibItemName()} at ({x}, {y}) rot: {fp.GetOrientation().AsDegrees()}")
    if abs(x - 30.90) < 1.0 and abs(y - 26.58) < 1.0:
        print(f"Ref: {fp.GetReference()} Val: {fp.GetValue()} FP: {fp.GetFPID().GetLibItemName()} at ({x}, {y}) rot: {fp.GetOrientation().AsDegrees()}")
