import pcbnew

board = pcbnew.LoadBoard("VFBMS32.kicad_pcb")
fps = board.GetFootprints()
print(f"Total footprints: {len(fps)}")
for fp in sorted(fps, key=lambda f: f.GetReference()):
    p = fp.GetPosition()
    x, y = pcbnew.ToMM(p.x), pcbnew.ToMM(p.y)
    print(f"{fp.GetReference():12} {fp.GetValue():15} {str(fp.GetFPID().GetLibItemName()):25} ({x:6.2f}, {y:6.2f})")
