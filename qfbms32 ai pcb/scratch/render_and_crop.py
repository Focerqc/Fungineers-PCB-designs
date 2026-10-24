import subprocess
import os
from PIL import Image

kicad_cli = r"C:\Program Files\KiCad\10.0\bin\kicad-cli.exe"
pcb_path = "qfbms32.kicad_pcb"
test_render = "scratch/test_render_parts.png"

subprocess.run([
    kicad_cli, "pcb", "render",
    "--side", "top",
    "--width", "4000",
    "--height", "1200",
    "--background", "transparent",
    "-o", test_render,
    pcb_path
], check=True)

im = Image.open(test_render)
bbox = im.getbbox()
if bbox:
    cropped = im.crop(bbox)
    w, h = cropped.size
    print(f"Cropped board size: {w}x{h}")
    # X=30.85 / 130 = 0.237, Y=28.2 / 32 = 0.881
    cx = int(30.85 / 130.0 * w)
    cy = int(28.2 / 32.0 * h)
    
    crop = cropped.crop((cx - 150, cy - 120, cx + 150, cy + 120))
    crop.save("scratch/crop_rendered_new_parts.png")
    print("Saved crop_rendered_new_parts.png")
