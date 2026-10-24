import pcbnew

board = pcbnew.LoadBoard('qfbms32.kicad_pcb')

print("=== Items near (15.1, 1.13) ===")
# check pads
for fp in board.GetFootprints():
    for pad in fp.Pads():
        pos = pad.GetPosition()
        x = pcbnew.ToMM(pos.x)
        y = pcbnew.ToMM(pos.y)
        if abs(x - 15.1) < 5 and abs(y - 1.13) < 5:
            print(f"Pad: {fp.GetReference()} pad {pad.GetName()} at ({x:.2f}, {y:.2f}) net={pad.GetNetname()}")

# check tracks
for track in board.GetTracks():
    start = track.GetStart()
    end = track.GetEnd()
    sx, sy = pcbnew.ToMM(start.x), pcbnew.ToMM(start.y)
    ex, ey = pcbnew.ToMM(end.x), pcbnew.ToMM(end.y)
    if (abs(sx - 15.1) < 5 and abs(sy - 1.13) < 5) or (abs(ex - 15.1) < 5 and abs(ey - 1.13) < 5):
        print(f"Track: ({sx:.2f}, {sy:.2f}) -> ({ex:.2f}, {ey:.2f}) net={track.GetNetname()}")

# check zones
for zone in board.Zones():
    if zone.HitTest(pcbnew.VECTOR2I(pcbnew.FromMM(15.1), pcbnew.FromMM(1.13))):
        print(f"Zone hit at (15.1, 1.13): net={zone.GetNetname()} layer={board.GetLayerName(zone.GetLayer())}")

print("=== Items near (13.4, 30.7) ===")
for fp in board.GetFootprints():
    for pad in fp.Pads():
        pos = pad.GetPosition()
        x = pcbnew.ToMM(pos.x)
        y = pcbnew.ToMM(pos.y)
        if abs(x - 13.4) < 5 and abs(y - 30.7) < 5:
            print(f"Pad: {fp.GetReference()} pad {pad.GetName()} at ({x:.2f}, {y:.2f}) net={pad.GetNetname()}")
for zone in board.Zones():
    if zone.HitTest(pcbnew.VECTOR2I(pcbnew.FromMM(13.4), pcbnew.FromMM(30.7))):
        print(f"Zone hit at (13.4, 30.7): net={zone.GetNetname()} layer={board.GetLayerName(zone.GetLayer())}")
