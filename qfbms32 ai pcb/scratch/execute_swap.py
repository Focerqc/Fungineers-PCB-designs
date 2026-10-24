import pcbnew
import os
import shutil
import subprocess
from PIL import Image

pcb_dir = r"c:\Users\quinn\Documents\GitHub\Fungineers PCB designs\qfbms32 ai pcb"
pcb_path = os.path.join(pcb_dir, "qfbms32.kicad_pcb")

# Load board
board = pcbnew.LoadBoard(pcb_path)

# Template 0805 resistor footprint
template = board.FindFootprintByReference("R_B1")
if not template:
    template = board.FindFootprintByReference("R_CHG2")
if not template:
    raise RuntimeError("Could not find an existing R_0805_2012Metric template footprint on board")

# Remove any old versions of C_S1, C_S2, R_S1, R_S2
for ref in ["C_S1", "C_S2", "R_S1", "R_S2"]:
    fp = board.FindFootprintByReference(ref)
    if fp:
        print(f"Removing existing {ref}")
        board.Remove(fp)

# Create R_S1
fp1 = pcbnew.FOOTPRINT(template)
fp1.SetUuid(pcbnew.KIID())
fp1.SetReference("R_S1")
fp1.SetValue("1000")
fp1.SetPosition(pcbnew.VECTOR2I(pcbnew.FromMM(17.63), pcbnew.FromMM(15.00)))
fp1.SetOrientation(pcbnew.EDA_ANGLE(0.0, pcbnew.DEGREES_T))
fp1.Reference().SetVisible(False)
fp1.Value().SetVisible(False)
for pad in fp1.Pads():
    pad.SetUuid(pcbnew.KIID())
    pad.SetNetCode(0)
board.Add(fp1)
print(f"Added R_S1 (Val: 1000, FP: R_0805_2012Metric) at (17.630, 15.000)")

# Create R_S2
fp2 = pcbnew.FOOTPRINT(template)
fp2.SetUuid(pcbnew.KIID())
fp2.SetReference("R_S2")
fp2.SetValue("1000")
fp2.SetPosition(pcbnew.VECTOR2I(pcbnew.FromMM(17.50), pcbnew.FromMM(17.00)))
fp2.SetOrientation(pcbnew.EDA_ANGLE(0.0, pcbnew.DEGREES_T))
fp2.Reference().SetVisible(False)
fp2.Value().SetVisible(False)
for pad in fp2.Pads():
    pad.SetUuid(pcbnew.KIID())
    pad.SetNetCode(0)
board.Add(fp2)
print(f"Added R_S2 (Val: 1000, FP: R_0805_2012Metric) at (17.500, 17.000)")

# Save board
pcbnew.SaveBoard(pcb_path, board)
print("Board saved successfully to:", pcb_path)

# Render raw top view
kicad_cli = r"C:\Program Files\KiCad\10.0\bin\kicad-cli.exe"
raw_top_png = os.path.join(pcb_dir, "qfbms32_layout_top_hi_raw.png")
top_3d_png = os.path.join(pcb_dir, "qfbms32_3d_top.png")

print("Rendering top view with kicad-cli...")
res = subprocess.run([
    kicad_cli, "pcb", "render",
    "--side", "top",
    "--width", "3600", "--height", "1200",
    "--background", "transparent",
    "-o", raw_top_png, pcb_path
], capture_output=True, text=True)

if res.returncode != 0:
    print("Render warning/error:", res.stderr)
else:
    print("Render completed.")

# Autocrop transparent margins and save 3d top
if os.path.exists(raw_top_png):
    im = Image.open(raw_top_png)
    bbox = im.getbbox()
    if bbox:
        pad = 30
        box = (max(0, bbox[0]-pad), max(0, bbox[1]-pad), min(im.width, bbox[2]+pad), min(im.height, bbox[3]+pad))
        cropped = im.crop(box)
        cropped.save(raw_top_png)
        cropped.save(top_3d_png)
        print(f"Updated {top_3d_png}: size {cropped.size}")

# Update annotated preview
current_brain = r"C:\Users\quinn\.gemini\antigravity-ide\brain\0b8fcda9-1947-42aa-99e4-1151d2cb92f0"
os.makedirs(current_brain, exist_ok=True)

import sys
sys.path.insert(0, pcb_dir)
import generate_annotated_preview
generate_annotated_preview.generate_annotated_preview()

# Copy to current brain dir
shutil.copy(top_3d_png, os.path.join(current_brain, "qfbms32_3d_top.png"))
shutil.copy(os.path.join(pcb_dir, "qfbms32_layout_labeled.png"), os.path.join(current_brain, "qfbms32_layout_labeled.png"))

print("All previews updated and copied to brain directory.")
