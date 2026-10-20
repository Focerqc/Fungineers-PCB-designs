import os
import pcbnew

project_dir = r"c:\Users\quinn\Documents\GitHub\Fungineers PCB designs\Q VFBMS32 AI PCB"
pcb_path = os.path.join(project_dir, "VFBMS32.kicad_pcb")
kicad_fp_dir = r"C:\Program Files\KiCad\10.0\share\kicad\footprints"

board = pcbnew.LoadBoard(pcb_path)

# 1. Remove old dummy footprints D_V1, D_V2, D_V3 if present
removed = []
for ref in ['D_V1', 'D_V2', 'D_V3']:
    fp = board.FindFootprintByReference(ref)
    if fp:
        board.Delete(fp)
        removed.append(ref)
print(f"Removed dummy footprints: {removed}")

# 2. Add 100k 0603 resistor R_CHG1
res_lib = os.path.join(kicad_fp_dir, "Resistor_SMD.pretty")
r_fp = board.FindFootprintByReference("R_CHG1")
if r_fp:
    board.Delete(r_fp)

r_fp = pcbnew.FootprintLoad(res_lib, "R_0603_1608Metric")
board.Add(r_fp)
r_fp.SetReference("R_CHG1")
r_fp.SetValue("100k")
r_fp.SetPosition(pcbnew.VECTOR2I(pcbnew.FromMM(1.30), pcbnew.FromMM(15.75)))
r_fp.SetOrientation(pcbnew.EDA_ANGLE(90.0, pcbnew.DEGREES_T))
r_fp.Reference().SetVisible(True)
r_fp.Reference().SetTextSize(pcbnew.VECTOR2I(pcbnew.FromMM(0.65), pcbnew.FromMM(0.65)))
r_fp.Reference().SetTextThickness(pcbnew.FromMM(0.12))
r_fp.Value().SetVisible(False)
print("Placed R_CHG1 (100k 0603) at (1.30, 15.75)")

# 3. Add the three DSK320 (K320) Schottky diodes in SOD-123FL
diode_lib = os.path.join(kicad_fp_dir, "Diode_SMD.pretty")
diode_coords = [
    ("D_CHG1", 3.15),
    ("D_CHG2", 4.90),
    ("D_CHG3", 6.65),
]

for ref, x in diode_coords:
    old = board.FindFootprintByReference(ref)
    if old:
        board.Delete(old)

    d_fp = pcbnew.FootprintLoad(diode_lib, "D_SOD-123F")
    board.Add(d_fp)
    d_fp.SetReference(ref)
    d_fp.SetValue("DSK320")
    d_fp.SetPosition(pcbnew.VECTOR2I(pcbnew.FromMM(x), pcbnew.FromMM(15.75)))
    d_fp.SetOrientation(pcbnew.EDA_ANGLE(270.0, pcbnew.DEGREES_T))
    d_fp.Reference().SetVisible(True)
    d_fp.Reference().SetTextSize(pcbnew.VECTOR2I(pcbnew.FromMM(0.65), pcbnew.FromMM(0.65)))
    d_fp.Reference().SetTextThickness(pcbnew.FromMM(0.12))
    d_fp.Value().SetVisible(False)
    print(f"Placed {ref} (DSK320 SOD-123F) at ({x:.2f}, 15.75)")

# Save board
pcbnew.SaveBoard(pcb_path, board)
print("VFBMS32.kicad_pcb updated and saved successfully!")
