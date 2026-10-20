import pcbnew

pcb_path = r"c:\Users\quinn\Documents\GitHub\Fungineers PCB designs\Q VFBMS32 AI PCB\VFBMS32.kicad_pcb"
board = pcbnew.LoadBoard(pcb_path)

for ref in ['J_CHG1', 'J_BAT1', 'C_FLT1', 'D_V1']:
    fp = board.FindFootprintByReference(ref)
    if fp:
        print(f"\nFootprint {ref}:")
        for pad in fp.Pads():
            net = pad.GetNet()
            net_name = net.GetNetname() if net else "NO_NET"
            pos = pad.GetPosition()
            print(f"  Pad {pad.GetName()}: Net='{net_name}' at ({pcbnew.ToMM(pos.x):.2f}, {pcbnew.ToMM(pos.y):.2f})")
