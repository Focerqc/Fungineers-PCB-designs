import pcbnew
import os

pcb_path = "qfbms32.kicad_pcb"
board = pcbnew.LoadBoard(pcb_path)

# Check and remove if previously added
for ref in ["R_DSG1", "U_COMM_PASS1", "R_1000", "FB1"]:
    fp = board.FindFootprintByReference(ref)
    if fp:
        board.Remove(fp)

kicad_fp_dir = r"C:\Program Files\KiCad\10.0\share\kicad\footprints\Resistor_SMD.pretty"

# 1. Color 1: 0805 "1000" at (30.78, 29.83) rot=90
fp1 = pcbnew.FootprintLoad(kicad_fp_dir, "R_0805_2012Metric")
board.Add(fp1)
fp1.SetReference("R_DSG1")
fp1.SetValue("1000")
fp1.SetPosition(pcbnew.VECTOR2I(pcbnew.FromMM(30.78), pcbnew.FromMM(29.83)))
fp1.SetOrientation(pcbnew.EDA_ANGLE(90.0, pcbnew.DEGREES_T))
fp1.Reference().SetVisible(False)
fp1.Value().SetVisible(False)

# 2. Color 2: 0603 "Unmarked" at (30.90, 26.58) rot=90
fp2 = pcbnew.FootprintLoad(kicad_fp_dir, "R_0603_1608Metric")
board.Add(fp2)
fp2.SetReference("FB1")
fp2.SetValue("Unmarked")
fp2.SetPosition(pcbnew.VECTOR2I(pcbnew.FromMM(30.90), pcbnew.FromMM(26.58)))
fp2.SetOrientation(pcbnew.EDA_ANGLE(90.0, pcbnew.DEGREES_T))
fp2.Reference().SetVisible(False)
fp2.Value().SetVisible(False)

pcbnew.SaveBoard(pcb_path, board)
print("Successfully added R_DSG1 (1000) and FB1 (Unmarked)")
