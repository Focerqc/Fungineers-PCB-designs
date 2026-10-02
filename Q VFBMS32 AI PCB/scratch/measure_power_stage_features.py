import pcbnew

board = pcbnew.LoadBoard(r"c:\Users\quinn\Desktop\AI PCB CAD\Q VFBMS32 AI PCB\VFBMS32.kicad_pcb")

print("Current Power Stage Placements:")
for ref in ["J_CHG1", "J_BAT1", "Q1", "Q2", "F1", "R_SH1", "R_SH2", "C_DISC", "U_SSR1", "U_BQ2"]:
    fp = board.FindFootprintByReference(ref)
    if fp:
        p = fp.GetPosition()
        print(f"  {ref:8s}: ({pcbnew.ToMM(p.x):6.2f}, {pcbnew.ToMM(p.y):6.2f}) rot={fp.GetOrientationDegrees():5.1f}")
