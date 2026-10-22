import pcbnew

board = pcbnew.LoadBoard(r"c:\Users\quinn\Documents\GitHub\Fungineers PCB designs\qfbms32 ai pcb\qfbms32.kicad_pcb")

print("--- TRACKS IN REGION X: 40-85, Y: 0-25 ---")
for t in board.GetTracks():
    sp = t.GetStart()
    ep = t.GetEnd()
    sx, sy = sp.x / 1e6, sp.y / 1e6
    ex, ey = ep.x / 1e6, ep.y / 1e6
    layer = board.GetLayerName(t.GetLayer())
    if 40 < sx < 85 and 0 < sy < 25:
        if isinstance(t, pcbnew.PCB_VIA):
            print(f"VIA at ({sx:.2f}, {sy:.2f}) drill={t.GetDrill()/1e6:.2f}")
        else:
            print(f"{layer:8}: ({sx:6.2f}, {sy:6.2f}) -> ({ex:6.2f}, {ey:6.2f})")
