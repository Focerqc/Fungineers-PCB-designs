import subprocess
import os
from PIL import Image

pcb_path = r"c:\Users\quinn\Desktop\AI PCB CAD\Q VFBMS32 AI PCB\VFBMS32.kicad_pcb"
kicad_cli = r"C:\Program Files\KiCad\10.0\bin\kicad-cli.exe"

# We want to test XT30PW-M orientations
# Options for rotation around X, Y, Z:
candidates = [
    ("m_rot_0_0_90", "0 0 90", "0 0 0"),
    ("m_rot_180_0_90", "180 0 90", "0 0 0"),
    ("m_rot_180_0_neg90", "180 0 -90", "0 0 0"),
    ("m_rot_0_180_90", "0 180 90", "0 0 0"),
    ("m_rot_0_0_neg90", "0 0 -90", "0 0 0"),
]

for tag, rot_m, off_m in candidates:
    with open(pcb_path, "r", encoding="utf-8") as f:
        txt = f.read()

    # Replace model block for XT30PW-M
    idx = txt.find('(footprint "XT30PW-M_Lugs"')
    if idx == -1:
        continue
    end_idx = txt.find('(footprint "', idx + 10)
    sub = txt[idx:end_idx]
    
    # replace offset and rotate
    import re
    sub_new = re.sub(r'\(offset\s*\(xyz\s*[-0-9. ]+\)\s*\)', f'(offset (xyz {off_m}))', sub)
    sub_new = re.sub(r'\(rotate\s*\(xyz\s*[-0-9. ]+\)\s*\)', f'(rotate (xyz {rot_m}))', sub_new)
    
    txt_new = txt[:idx] + sub_new + txt[end_idx:]
    with open(pcb_path, "w", encoding="utf-8") as f:
        f.write(txt_new)
        
    out_img = f"test_{tag}.png"
    subprocess.run([
        kicad_cli, "pcb", "render",
        "--side", "top",
        "--width", "1200", "--height", "400",
        "--background", "transparent",
        "-o", out_img, pcb_path
    ], check=True)
    
    im = Image.open(out_img)
    bbox = im.getbbox()
    if bbox:
        # crop bottom-left corner
        crop = im.crop((bbox[0], bbox[3] - 180, bbox[0] + 300, bbox[3]))
        crop.save(f"crop_{tag}.png")
        print(f"Generated crop_{tag}.png")

