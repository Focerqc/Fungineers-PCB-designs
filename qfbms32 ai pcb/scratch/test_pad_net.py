import pcbnew

board = pcbnew.LoadBoard("qfbms32 ai pcb/qfbms32.kicad_pcb")
template_fp = board.FindFootprintByReference("R_B1")
clone = pcbnew.FOOTPRINT(template_fp)

# Check pads
for pad in clone.Pads():
    print(f"Before clearing: pad {pad.GetName()} net={pad.GetNetname()}")
    pad.SetNetCode(0)
    print(f"After clearing: pad {pad.GetName()} net={pad.GetNetname()}")
