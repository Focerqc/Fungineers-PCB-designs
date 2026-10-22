import pcbnew

board = pcbnew.BOARD()
zone = pcbnew.ZONE(board)
zone.SetLayer(pcbnew.F_Cu)

outline = zone.Outline()
poly = pcbnew.SHAPE_LINE_CHAIN()
poly.Append(pcbnew.FromMM(10), pcbnew.FromMM(10))
poly.Append(pcbnew.FromMM(20), pcbnew.FromMM(10))
poly.Append(pcbnew.FromMM(20), pcbnew.FromMM(20))
poly.Append(pcbnew.FromMM(10), pcbnew.FromMM(20))
poly.SetClosed(True)

outline.AddOutline(poly)
zone.SetIsFilled(True)
board.Add(zone)

filler = pcbnew.ZONE_FILLER(board)
filler.Fill(board.Zones())
print("Zone filled successfully, outline count:", outline.OutlineCount())
