import pcbnew

board = pcbnew.BOARD()
s = pcbnew.PCB_SHAPE(board)
s.SetShape(pcbnew.SHAPE_T_POLY)
s.SetLayer(pcbnew.F_Cu)
s.SetFilled(True)

poly = pcbnew.SHAPE_LINE_CHAIN()
poly.Append(pcbnew.FromMM(5), pcbnew.FromMM(5))
poly.Append(pcbnew.FromMM(20), pcbnew.FromMM(5))
poly.Append(pcbnew.FromMM(20), pcbnew.FromMM(10))
poly.Append(pcbnew.FromMM(5), pcbnew.FromMM(10))
poly.SetClosed(True)

s.SetPolyShape(pcbnew.SHAPE_POLY_SET(poly))
board.Add(s)

print("Copper shape created successfully!")
