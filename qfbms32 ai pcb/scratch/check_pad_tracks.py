import pcbnew

board = pcbnew.LoadBoard("qfbms32 ai pcb/qfbms32.kicad_pcb")

c_s1 = board.FindFootprintByReference("C_S1")
c_s2 = board.FindFootprintByReference("C_S2")

for fp, name in [(c_s1, "C_S1"), (c_s2, "C_S2")]:
    if not fp:
        print(f"{name} not found!")
        continue
    for pad in fp.Pads():
        p = pad.GetPosition()
        px, py = pcbnew.ToMM(p.x), pcbnew.ToMM(p.y)
        print(f"{name} pad {pad.GetName()} at ({px:.3f}, {py:.3f})")
        # Check if any track touches this pad
        for track in board.GetTracks():
            t1 = track.GetStart()
            t2 = track.GetEnd()
            d1 = (pcbnew.ToMM(t1.x) - px)**2 + (pcbnew.ToMM(t1.y) - py)**2
            d2 = (pcbnew.ToMM(t2.x) - px)**2 + (pcbnew.ToMM(t2.y) - py)**2
            if d1 < 0.2**2 or d2 < 0.2**2:
                print(f"   Connected track: ({pcbnew.ToMM(t1.x):.2f}, {pcbnew.ToMM(t1.y):.2f}) -> ({pcbnew.ToMM(t2.x):.2f}, {pcbnew.ToMM(t2.y):.2f}) net={track.GetNetname()}")
