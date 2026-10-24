import os
import shutil
import subprocess
from PIL import Image

pcb_dir = r"c:\Users\quinn\Documents\GitHub\Fungineers PCB designs\qfbms32 ai pcb"
pcb_path = os.path.join(pcb_dir, "qfbms32.kicad_pcb")

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
