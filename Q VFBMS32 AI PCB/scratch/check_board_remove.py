import pcbnew

board = pcbnew.LoadBoard(r"c:\Users\quinn\Desktop\AI PCB CAD\Q VFBMS32 AI PCB\VFBMS32.kicad_pcb")

fp = board.FindFootprintByReference("U_BOOST1")
print("fp type:", type(fp))
print("board Remove methods:", [m for m in dir(board) if "remove" in m.lower() or "delete" in m.lower()])
