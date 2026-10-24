import pcbnew

board = pcbnew.LoadBoard('qfbms32.kicad_pcb.with_traces.bak')
print("Tracks count in backup:", len(board.GetTracks()))
for track in board.GetTracks():
    start = track.GetStart()
    end = track.GetEnd()
    sx, sy = pcbnew.ToMM(start.x), pcbnew.ToMM(start.y)
    ex, ey = pcbnew.ToMM(end.x), pcbnew.ToMM(end.y)
    if (25 <= sx <= 35 and 20 <= sy <= 32) or (25 <= ex <= 35 and 20 <= ey <= 32):
        print(f"Track: ({sx:.2f}, {sy:.2f}) -> ({ex:.2f}, {ey:.2f}) net={track.GetNetname()}")
