import pcbnew

board = pcbnew.BOARD()
t = pcbnew.PCB_TRACK(board)
t.SetLayer(pcbnew.F_Cu)
t.SetStart(pcbnew.VECTOR2I(pcbnew.FromMM(5), pcbnew.FromMM(5)))
t.SetEnd(pcbnew.VECTOR2I(pcbnew.FromMM(20), pcbnew.FromMM(5)))
t.SetWidth(pcbnew.FromMM(3.5))
board.Add(t)

print("Track created, width:", t.GetWidth())
