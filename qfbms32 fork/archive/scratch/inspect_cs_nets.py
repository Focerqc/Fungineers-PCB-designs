import pcbnew

board = pcbnew.LoadBoard("qfbms32 ai pcb/qfbms32.kicad_pcb")

for ref in ["C_S1", "C_S2", "D_S1"]:
    fp = board.FindFootprintByReference(ref)
    if fp:
        print(f"Footprint {ref}: {fp.GetFPID().GetLibItemName()} at {fp.GetPosition()} rot {fp.GetOrientation().AsDegrees()}")
        for pad in fp.Pads():
            net = pad.GetNet()
            net_name = net.GetNetname() if net else "NO_NET"
            pos = pad.GetPosition()
            print(f"  Pad {pad.GetName()}: net '{net_name}', pos ({pcbnew.ToMM(pos.x):.3f}, {pcbnew.ToMM(pos.y):.3f})")

# Also find all tracks with net or overlapping pads
for track in board.GetTracks():
    # check start and end
    p_start = track.GetStart()
    p_end = track.GetEnd()
    # if near 17.5, 15..17
    x_mid = pcbnew.ToMM((p_start.x + p_end.x) / 2)
    y_mid = pcbnew.ToMM((p_start.y + p_end.y) / 2)
    if 16.0 <= x_mid <= 19.0 and 14.0 <= y_mid <= 18.0:
        net = track.GetNet()
        net_name = net.GetNetname() if net else "NO_NET"
        print(f"Track: net '{net_name}' from ({pcbnew.ToMM(p_start.x):.2f}, {pcbnew.ToMM(p_start.y):.2f}) to ({pcbnew.ToMM(p_end.x):.2f}, {pcbnew.ToMM(p_end.y):.2f})")
