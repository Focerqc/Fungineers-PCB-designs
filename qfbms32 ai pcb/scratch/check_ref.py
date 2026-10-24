import pcbnew

board = pcbnew.LoadBoard("qfbms32 ai pcb/qfbms32.kicad_pcb")
fp = board.FindFootprintByReference("R_B1")
ref_text = fp.Reference()
print("Type of ref_text:", type(ref_text))
print("Dir of ref_text:", [m for m in dir(ref_text) if "vis" in m.lower()])
