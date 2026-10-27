import pcbnew

board = pcbnew.LoadBoard('qfbms32.kicad_pcb')
fps = list(board.GetFootprints())
print(f"Total footprints: {len(fps)}")
for fp in sorted(fps, key=lambda f: f.GetReference()):
    pos = fp.GetPosition()
    x = pcbnew.ToMM(pos.x)
    y = pcbnew.ToMM(pos.y)
    rot = fp.GetOrientationDegrees()
    print(f"{fp.GetReference():12s} {fp.GetValue():20s} pos=({x:6.2f}, {y:6.2f}) rot={rot:5.1f} fp={fp.GetFPID().GetLibItemName()}")
