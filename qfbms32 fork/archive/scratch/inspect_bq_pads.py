import pcbnew

pcb_path = r"c:\Users\quinn\Desktop\AI PCB CAD\Q VFBMS32 AI PCB\VFBMS32.kicad_pcb"
board = pcbnew.LoadBoard(pcb_path)

for ref in ["U_BQ1", "U_BQ2"]:
    fp = board.FindFootprintByReference(ref)
    if fp:
        print(f"\n{ref} pos: ({fp.GetPosition().x/1e6}, {fp.GetPosition().y/1e6})")
        pads = list(fp.Pads())
        print(f"Total pads: {len(pads)}")
        for p in pads[:12]:
            pos = p.GetPosition()
            print(f"  Pad {p.GetName()}: ({pos.x/1e6:.3f}, {pos.y/1e6:.3f})")
