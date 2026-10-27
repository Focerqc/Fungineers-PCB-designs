import pcbnew
import os
import shutil
import subprocess
from PIL import Image

pcb_dir = r"c:\Users\quinn\Documents\GitHub\Fungineers PCB designs\qfbms32 ai pcb"
pcb_path = os.path.join(pcb_dir, "qfbms32.kicad_pcb")

# 1. Create a safe backup before editing
bak_path = os.path.join(pcb_dir, ".history", "qfbms32_pre_col1_col2.kicad_pcb")
os.makedirs(os.path.dirname(bak_path), exist_ok=True)
shutil.copy2(pcb_path, bak_path)
print(f"Backed up board to {bak_path}")

board = pcbnew.LoadBoard(pcb_path)
kicad_fp_dir = r"C:\Program Files\KiCad\10.0\share\kicad\footprints\Resistor_SMD.pretty"

# Parts to place:
# Color 1 (#4ea1ff): 0603? "X10 or XIO maybe markings"
# 1. Box 1: (29.75, 17.20)
# 2. Box 2: (29.50, 7.60)
# 3. Box 3: (29.20, 4.05)
# Color 2 (#ff6b6b): 0603 "474 underlined"
# 1. Box 1: (29.50, 8.95)

new_parts = [
    {
        "ref": "R_SEC1",
        "alt_refs": ["R_SEC1", "R_CHG6", "R_BOX1"],
        "val": "01X",
        "desc": "Secondary / discharge snubber resistor (Color 1 Box 1)",
        "x": 29.75,
        "y": 17.20,
        "rot": 0.0
    },
    {
        "ref": "R_G1",
        "alt_refs": ["R_G1", "R_CHG3", "R_BOX2"],
        "val": "01X",
        "desc": "Q1 CHG FET Gate drive resistor (Color 1 Box 2)",
        "x": 29.50,
        "y": 7.60,
        "rot": 0.0
    },
    {
        "ref": "R_SSR1",
        "alt_refs": ["R_SSR1", "R_CHG5", "R_BOX3"],
        "val": "01X",
        "desc": "SSRelay precharge control resistor (Color 1 Box 3)",
        "x": 29.20,
        "y": 4.05,
        "rot": 0.0
    },
    {
        "ref": "R_GS1",
        "alt_refs": ["R_GS1", "R_CHG4", "R_BOX4"],
        "val": "474",
        "desc": "Q1 Gate-Source pull-down resistor 470k (Color 2 Box 1)",
        "x": 29.50,
        "y": 8.95,
        "rot": 0.0
    }
]

# Remove any previous instances
for p in new_parts:
    for ref_to_check in p["alt_refs"]:
        fp = board.FindFootprintByReference(ref_to_check)
        if fp:
            pos = fp.GetPosition()
            print(f"Removing existing footprint {ref_to_check} at ({pcbnew.ToMM(pos.x):.3f}, {pcbnew.ToMM(pos.y):.3f})")
            board.Remove(fp)

# Place new 0603 footprints
for p in new_parts:
    fp = pcbnew.FootprintLoad(kicad_fp_dir, "R_0603_1608Metric")
    if not fp:
        raise RuntimeError(f"Failed to load R_0603_1608Metric footprint from {kicad_fp_dir}")
    board.Add(fp)
    fp.SetReference(p["ref"])
    fp.SetValue(p["val"])
    fp.SetPosition(pcbnew.VECTOR2I(pcbnew.FromMM(p["x"]), pcbnew.FromMM(p["y"])))
    fp.SetOrientation(pcbnew.EDA_ANGLE(p["rot"], pcbnew.DEGREES_T))
    fp.Reference().SetVisible(False)
    fp.Value().SetVisible(False)
    print(f"Added {p['ref']} (Val: {p['val']}) at ({p['x']:.3f}, {p['y']:.3f}) rot={p['rot']:.1f}° - {p['desc']}")

# Save updated board
pcbnew.SaveBoard(pcb_path, board)
print("Board saved successfully to:", pcb_path)

# Render updated raw top image
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
brain_dir = r"C:\Users\quinn\.gemini\antigravity-ide\brain\7bc5fde5-e6cf-413a-9764-f83c0e8df3ae"
os.makedirs(brain_dir, exist_ok=True)

import sys
sys.path.insert(0, pcb_dir)
import generate_annotated_preview
generate_annotated_preview.generate_annotated_preview()

# Copy artifacts to current brain directory
shutil.copy2(top_3d_png, os.path.join(brain_dir, "qfbms32_3d_top.png"))
shutil.copy2(os.path.join(pcb_dir, "qfbms32_layout_labeled.png"), os.path.join(brain_dir, "qfbms32_layout_labeled.png"))

print("All previews updated and copied to brain directory.")
