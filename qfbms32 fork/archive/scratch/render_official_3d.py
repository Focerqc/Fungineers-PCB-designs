import subprocess
import os
from PIL import Image

kicad_cli = r"C:\Program Files\KiCad\10.0\bin\kicad-cli.exe"
pcb_path = "qfbms32.kicad_pcb"
out_png = "qfbms32_3d_top.png"

subprocess.run([
    kicad_cli, "pcb", "render",
    "--side", "top",
    "--width", "4000",
    "--height", "1200",
    "--background", "transparent",
    "-o", "scratch/raw_3d_top.png",
    pcb_path
], check=True)

im = Image.open("scratch/raw_3d_top.png")
bbox = im.getbbox()
if bbox:
    pad_x = 25
    pad_y = 15
    box = (
        max(0, bbox[0] - pad_x),
        max(0, bbox[1] - pad_y),
        min(im.width, bbox[2] + pad_x),
        min(im.height, bbox[3] + pad_y)
    )
    cropped = im.crop(box)
    cropped.save(out_png)
    print(f"Saved {out_png} size: {cropped.size}")
