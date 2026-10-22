import pcbnew

board = pcbnew.LoadBoard(r"c:\Users\quinn\Desktop\AI PCB CAD\Q VFBMS32 AI PCB\VFBMS32.kicad_pcb")

fp = board.FindFootprintByReference("J_CHG1")
print("J_CHG1 type:", type(fp), fp)
print("GetPosition:", fp.GetPosition())
board.Delete(fp)
print("Deleted J_CHG1")
fp2 = board.FindFootprintByReference("J_CHG1")
print("After delete, J_CHG1 is:", fp2)
