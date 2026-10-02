import subprocess
import os
from PIL import Image

pcb_path = r"c:\Users\quinn\Desktop\AI PCB CAD\Q VFBMS32 AI PCB\VFBMS32.kicad_pcb"
kicad_cli = r"C:\Program Files\KiCad\10.0\bin\kicad-cli.exe"

rotations = [
    ("rot_0_0_neg90", "0 0 -90"),
    ("rot_0_180_90", "0 180 90"),
    ("rot_0_180_neg90", "0 180 -90"),
    ("rot_180_0_90", "180 0 90"),
]

for tag, rot in rotations:
    with open(pcb_path, "r", encoding="utf-8") as f:
        txt = f.read()

    idx = txt.find('(footprint "XT30PW-M_Lugs"')
    end_idx = txt.find('(footprint "', idx + 10)
    sub = txt[idx:end_idx]
    
    import re
    sub_new = re.sub(r'\(rotate\s*\(xyz\s*[-0-9. ]+\)\s*\)', f'(rotate (xyz {rot}))', sub)
    txt_new = txt[:idx] + sub_new + txt[end_idx:]
    with open(pcb_path, "w", encoding="utf-8") as f:
        f.write(txt_new)
        
    out_img = f"m_{tag}.png"
    subprocess.run([
        kicad_cli, "pcb", "render",
        "--perspective", "--rotate", "-30,0,20",
        "--floor",
        "--width", "1600", "--height", "900",
        "--background", "transparent",
        "-o", out_img, pcb_path
    ], check=True)
    
    im = Image.open(out_img)
    bbox = im.getbbox()
    if bbox:
        im.crop((0, 300, 800, im.height)).save(f"crop_3d_{tag}.png")
        print(f"Generated crop_3d_{tag}.png")

