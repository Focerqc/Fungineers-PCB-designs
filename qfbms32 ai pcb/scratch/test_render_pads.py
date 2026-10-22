import pcbnew
import subprocess
from PIL import Image

board = pcbnew.LoadBoard(r"c:\Users\quinn\Desktop\AI PCB CAD\Q VFBMS32 AI PCB\VFBMS32.kicad_pcb")
custom_lib = r"c:\Users\quinn\Desktop\AI PCB CAD\Q VFBMS32 AI PCB\vfbms.pretty"

# Delete ghost ICs
for ref in ["U_BOOST1", "U_BUCK1"]:
    fp = board.FindFootprintByReference(ref)
    if fp:
        board.Delete(fp)

# Replace J_CHG1 and J_BAT1
for ref, lib_item in [("J_CHG1", "XT30PW-F_Lugs"), ("J_BAT1", "XT30PW-M_Lugs")]:
    old_fp = board.FindFootprintByReference(ref)
    pos = pcbnew.VECTOR2I(old_fp.GetPosition().x, old_fp.GetPosition().y)
    rot = old_fp.GetOrientation()
    val = old_fp.GetValue()
    board.Delete(old_fp)
    
    new_fp = pcbnew.FootprintLoad(custom_lib, lib_item)
    new_fp.SetPosition(pos)
    new_fp.SetOrientation(rot)
    new_fp.SetReference(ref)
    new_fp.SetValue(val)
    board.Add(new_fp)

# Shift Q1 and Q2 right to X = 21.50
for ref, new_x in [("Q1", 21.50), ("Q2", 21.50)]:
    fp = board.FindFootprintByReference(ref)
    p = fp.GetPosition()
    fp.SetPosition(pcbnew.VECTOR2I(pcbnew.FromMM(new_x), p.y))

# Also shift R_SH2 to X = 21.50
r_sh2 = board.FindFootprintByReference("R_SH2")
if r_sh2:
    p = r_sh2.GetPosition()
    r_sh2.SetPosition(pcbnew.VECTOR2I(pcbnew.FromMM(21.50), p.y))

# Save to test board in root directory so KIPRJMOD resolves 3dmodels properly!
test_pcb = r"c:\Users\quinn\Desktop\AI PCB CAD\Q VFBMS32 AI PCB\VFBMS32_test.kicad_pcb"
pcbnew.SaveBoard(test_pcb, board)

kicad_cli = r"C:\Program Files\KiCad\10.0\bin\kicad-cli.exe"

# 1. Side profile 3D render
out_side = r"c:\Users\quinn\Desktop\AI PCB CAD\Q VFBMS32 AI PCB\scratch\test_verif_side.png"
subprocess.run([
    kicad_cli, "pcb", "render",
    "--side", "left",
    "--width", "2400", "--height", "1200",
    "--background", "transparent",
    "-o", out_side,
    test_pcb
], check=True)

# 2. Top-down 2D render
out_top = r"c:\Users\quinn\Desktop\AI PCB CAD\Q VFBMS32 AI PCB\scratch\test_verif_top.png"
subprocess.run([
    kicad_cli, "pcb", "render",
    "--side", "top",
    "--width", "3600", "--height", "1200",
    "--background", "transparent",
    "-o", out_top,
    test_pcb
], check=True)

print("Test renders finished successfully!")
