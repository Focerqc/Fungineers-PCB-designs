import pcbnew
import os
import shutil
import subprocess
from PIL import Image

pcb_dir = r"c:\Users\quinn\Documents\GitHub\Fungineers PCB designs\qfbms32 ai pcb"
pcb_path = os.path.join(pcb_dir, "qfbms32.kicad_pcb")
kicad_fp_dir = r"C:\Program Files\KiCad\10.0\share\kicad\footprints\Resistor_SMD.pretty"

# 1. Load footprints first before loading board
fp1 = pcbnew.FootprintLoad(kicad_fp_dir, "R_0805_2012Metric")
fp2 = pcbnew.FootprintLoad(kicad_fp_dir, "R_0805_2012Metric")
if not fp1 or not fp2:
    raise RuntimeError("Failed to load R_0805_2012Metric footprint from library")

# 2. Load board
board = pcbnew.LoadBoard(pcb_path)

# 3. Remove old footprints
for ref in ["C_S1", "C_S2", "R_S1", "R_S2"]:
    fp = board.FindFootprintByReference(ref)
    if fp:
        print(f"Removing old {ref}")
        board.Remove(fp)

# 4. Add R_S1 (Box 1: X=17.625, Y=15.00, WxH=2.35x1.00, rot=0)
board.Add(fp1)
fp1.SetReference("R_S1")
fp1.SetValue("1000")
fp1.SetPosition(pcbnew.VECTOR2I(pcbnew.FromMM(17.625), pcbnew.FromMM(15.00)))
fp1.SetOrientation(pcbnew.EDA_ANGLE(0.0, pcbnew.DEGREES_T))
ref1 = board.FindFootprintByReference("R_S1")
ref1.Reference().SetVisible(False)
ref1.Value().SetVisible(False)
print("Successfully added R_S1 at (17.625, 15.000)")

# 5. Add R_S2 (Box 2: X=17.50, Y=17.00, WxH=2.40x0.90, rot=0)
board.Add(fp2)
fp2.SetReference("R_S2")
fp2.SetValue("1000")
fp2.SetPosition(pcbnew.VECTOR2I(pcbnew.FromMM(17.50), pcbnew.FromMM(17.00)))
fp2.SetOrientation(pcbnew.EDA_ANGLE(0.0, pcbnew.DEGREES_T))
ref2 = board.FindFootprintByReference("R_S2")
ref2.Reference().SetVisible(False)
ref2.Value().SetVisible(False)
print("Successfully added R_S2 at (17.500, 17.000)")

# 6. Save board
pcbnew.SaveBoard(pcb_path, board)
print("Board saved successfully to:", pcb_path)

# 7. Render raw top view
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

# 8. Autocrop transparent margins and save 3d top
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

# 9. Update annotated preview
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
