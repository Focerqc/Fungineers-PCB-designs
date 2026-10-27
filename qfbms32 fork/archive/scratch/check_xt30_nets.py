import pcbnew

board = pcbnew.LoadBoard(r"c:\Users\quinn\Desktop\AI PCB CAD\Q VFBMS32 AI PCB\VFBMS32.kicad_pcb")

for ref in ["J_CHG1", "J_BAT1"]:
    fp = board.FindFootprintByReference(ref)
    print(f"\n{ref} Nets:")
    for pad in fp.Pads():
        print(f"  Pad {pad.GetNumber()}: Net '{pad.GetNetname()}' (Netcode {pad.GetNetCode()})")
