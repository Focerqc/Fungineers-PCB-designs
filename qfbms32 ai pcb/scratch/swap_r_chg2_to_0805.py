import pcbnew
import os

pcb_path = "qfbms32.kicad_pcb"
board = pcbnew.LoadBoard(pcb_path)

fp_old = board.FindFootprintByReference("R_CHG2")
pos = pcbnew.VECTOR2I(pcbnew.FromMM(14.3), pcbnew.FromMM(1.1))
rot = pcbnew.EDA_ANGLE(0.0, pcbnew.DEGREES_T)

if fp_old:
    pos = fp_old.GetPosition()
    rot = fp_old.GetOrientation()
    val = fp_old.GetValue()
    print(f"Removing old R_CHG2 ({fp_old.GetFPID().GetLibItemName()}) at ({pcbnew.ToMM(pos.x):.3f}, {pcbnew.ToMM(pos.y):.3f})")
    board.Remove(fp_old)
else:
    val = "2203"

kicad_fp_dir = r"C:\Program Files\KiCad\10.0\share\kicad\footprints\Resistor_SMD.pretty"
fp_new = pcbnew.FootprintLoad(kicad_fp_dir, "R_0805_2012Metric")
if not fp_new:
    raise RuntimeError("Failed to load R_0805_2012Metric footprint")

board.Add(fp_new)
fp_new.SetReference("R_CHG2")
fp_new.SetValue("2203")
fp_new.SetPosition(pos)
fp_new.SetOrientation(rot)

# Reference / Value styling
fp_new.Reference().SetVisible(False)
fp_new.Value().SetVisible(False)

# Save
pcbnew.SaveBoard(pcb_path, board)
print(f"Successfully replaced R_CHG2 with R_0805_2012Metric at ({pcbnew.ToMM(pos.x):.3f}, {pcbnew.ToMM(pos.y):.3f})")
