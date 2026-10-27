import pcbnew
import os
import shutil
import subprocess
from PIL import Image

pcb_dir = r"c:\Users\quinn\Documents\GitHub\Fungineers PCB designs\qfbms32 ai pcb"
pcb_path = os.path.join(pcb_dir, "qfbms32.kicad_pcb")
board = pcbnew.LoadBoard(pcb_path)

kicad_fp_dir = r"C:\Program Files\KiCad\10.0\share\kicad\footprints\Resistor_SMD.pretty"

# Parts to update
updates = [
    {
        "old_refs": ["C_S1", "R_S1"],
        "new_ref": "R_S1",
        "val": "1000",
        "x": 17.625,
        "y": 15.00,
        "rot": 0.0
    },
    {
        "old_refs": ["C_S2", "R_S2"],
        "new_ref": "R_S2",
        "val": "1000",
        "x": 17.50,
        "y": 17.00,
        "rot": 0.0
    }
]

for u in updates:
    # Find and remove any existing
    for old_ref in u["old_refs"]:
        fp_old = board.FindFootprintByReference(old_ref)
        if fp_old:
            pos = fp_old.GetPosition()
            print(f"Removing old footprint {old_ref} ({fp_old.GetFPID().GetLibItemName()}) at ({pcbnew.ToMM(pos.x):.3f}, {pcbnew.ToMM(pos.y):.3f})")
            board.Remove(fp_old)

    # Load R_0805_2012Metric
    fp_new = pcbnew.FootprintLoad(kicad_fp_dir, "R_0805_2012Metric")
    if not fp_new:
        raise RuntimeError(f"Failed to load R_0805_2012Metric footprint from {kicad_fp_dir}")

    board.Add(fp_new)
    fp_new.SetReference(u["new_ref"])
    fp_new.SetValue(u["val"])
    fp_new.SetPosition(pcbnew.VECTOR2I(pcbnew.FromMM(u["x"]), pcbnew.FromMM(u["y"])))
    fp_new.SetOrientation(pcbnew.EDA_ANGLE(u["rot"], pcbnew.DEGREES_T))

    fp_new.Reference().SetVisible(False)
    fp_new.Value().SetVisible(False)
    print(f"Added {u['new_ref']} (Val: {u['val']}) at ({u['x']:.3f}, {u['y']:.3f}) rot={u['rot']}")

# Save updated board
pcbnew.SaveBoard(pcb_path, board)
print("Board saved successfully!")

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
sys_path = os.path.join(pcb_dir, "generate_annotated_preview.py")
current_brain = r"C:\Users\quinn\.gemini\antigravity-ide\brain\0b8fcda9-1947-42aa-99e4-1151d2cb92f0"
os.makedirs(current_brain, exist_ok=True)

import sys
sys.path.insert(0, pcb_dir)
import generate_annotated_preview
generate_annotated_preview.generate_annotated_preview()

# Copy artifacts to current brain directory
shutil.copy(top_3d_png, os.path.join(current_brain, "qfbms32_3d_top.png"))
shutil.copy(os.path.join(pcb_dir, "qfbms32_layout_labeled.png"), os.path.join(current_brain, "qfbms32_layout_labeled.png"))

print("All previews updated and copied to brain directory.")
