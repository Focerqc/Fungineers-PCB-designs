import pcbnew

pcb_path = r"c:\Users\quinn\Desktop\AI PCB CAD\Q VFBMS32 AI PCB\VFBMS32.kicad_pcb"
board = pcbnew.LoadBoard(pcb_path)

nets = board.GetNetsByName()
print(f"Total nets in board: {len(nets)}")
for name, net in list(nets.items())[:30]:
    print(f"Net: {name} (code {net.GetNetCode()})")

tracks = list(board.GetTracks())
print(f"Total tracks/vias in board: {len(tracks)}")
for t in tracks[:10]:
    print(f"Track: layer={t.GetLayerName()}, width={t.GetWidth()/1e6}mm, start=({t.GetStart().x/1e6}, {t.GetStart().y/1e6})")
