import subprocess
from PIL import Image

pcb_path = r"c:\Users\quinn\Desktop\AI PCB CAD\Q VFBMS32 AI PCB\VFBMS32.kicad_pcb"
kicad_cli = r"C:\Program Files\KiCad\10.0\bin\kicad-cli.exe"

# Test rotations for XT30PW-M
rotations = [
    ("rot_0_0_90", "0 0 90"),
    ("rot_180_0_90", "180 0 90"),
    ("rot_0_0_neg90", "0 0 -90"),
    ("rot_180_0_neg90", "180 0 -90"),
    ("rot_180_180_90", "180 180 90"),
    ("rot_0_180_neg90", "0 180 -90"),
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
        
    out_img = f"find_m_{tag}.png"
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
        im.crop((bbox[0], bbox[3] - 120, bbox[0] + 160, bbox[3])).save(f"thumb_m_{tag}.png")

print("All rendered!")
