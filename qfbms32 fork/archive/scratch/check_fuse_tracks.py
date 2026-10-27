import pcbnew

board = pcbnew.LoadBoard(r"c:\Users\quinn\Documents\GitHub\Fungineers PCB designs\Q VFBMS32 AI PCB\VFBMS32.kicad_pcb")

print("All tracks on board:")
for t in board.GetTracks():
    sp = t.GetStart()
    ep = t.GetEnd()
    sx, sy = sp.x / 1e6, sp.y / 1e6
    ex, ey = ep.x / 1e6, ep.y / 1e6
    print(f"{board.GetLayerName(t.GetLayer())}: ({sx:.2f}, {sy:.2f}) -> ({ex:.2f}, {ey:.2f}), width={t.GetWidth()/1e6:.2f}, net={t.GetNetname()}")
