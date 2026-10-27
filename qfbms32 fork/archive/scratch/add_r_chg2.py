import pcbnew
import os

pcb_path = "qfbms32.kicad_pcb"
board = pcbnew.LoadBoard(pcb_path)

# Check if R_CHG2 or any footprint already exists at (15.1, 1.13)
existing = board.FindFootprintByReference("R_CHG2")
if existing:
    print("Found existing R_CHG2, removing it first...")
    board.Remove(existing)

kicad_fp_dir = r"C:\Program Files\KiCad\10.0\share\kicad\footprints\Resistor_SMD.pretty"
fp = pcbnew.FootprintLoad(kicad_fp_dir, "R_1206_3216Metric")
if not fp:
    raise RuntimeError("Failed to load R_1206_3216Metric footprint")

board.Add(fp)
fp.SetReference("R_CHG2")
fp.SetValue("2203")
fp.SetPosition(pcbnew.VECTOR2I(pcbnew.FromMM(15.10), pcbnew.FromMM(1.125)))
fp.SetOrientation(pcbnew.EDA_ANGLE(0.0, pcbnew.DEGREES_T))

# Configure text visibility
# Keep reference hidden or visible small
fp.Reference().SetVisible(False)
fp.Value().SetVisible(False)

# Save board
pcbnew.SaveBoard(pcb_path, board)
print("Successfully added R_CHG2 to", pcb_path)

# Verify
board2 = pcbnew.LoadBoard(pcb_path)
fp2 = board2.FindFootprintByReference("R_CHG2")
pos = fp2.GetPosition()
print(f"Verified R_CHG2: ref={fp2.GetReference()}, val={fp2.GetValue()}, pos=({pcbnew.ToMM(pos.x):.3f}, {pcbnew.ToMM(pos.y):.3f}), rot={fp2.GetOrientationDegrees()}")
