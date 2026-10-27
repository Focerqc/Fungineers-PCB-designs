import subprocess
import re
from PIL import Image

pcb_path = r"c:\Users\quinn\Desktop\AI PCB CAD\Q VFBMS32 AI PCB\VFBMS32.kicad_pcb"
kicad_cli = r"C:\Program Files\KiCad\10.0\bin\kicad-cli.exe"

with open(pcb_path, "r", encoding="utf-8") as f:
    txt = f.read()

# Update XT30PW-M 3D model offset to (xyz 4.1 0 2.5)
txt_test = re.sub(
    r'(\(model "\$\{KIPRJMOD\}/3dmodels/XT30PW-M\.step"[\s\S]*?\(offset\s*\(xyz\s*)[-\d.]+(\s+[-\d.]+\s+)[-\d.]+(\s*\))',
    r'\g<1>4.1\g<2>2.5\g<3>',
    txt
)

test_pcb = r"c:\Users\quinn\Desktop\AI PCB CAD\Q VFBMS32 AI PCB\scratch\test_z.kicad_pcb"
with open(test_pcb, "w", encoding="utf-8") as f:
    f.write(txt_test)

out_png = r"c:\Users\quinn\Desktop\AI PCB CAD\Q VFBMS32 AI PCB\scratch\test_side_z25.png"
subprocess.run([
    kicad_cli, "pcb", "render",
    "--side", "left",
    "--width", "1600", "--height", "900",
    "--background", "transparent",
    "-o", out_png,
    test_pcb
], check=True)

im = Image.open(out_png)
bbox = im.getbbox()
if bbox:
    pad = 30
    crop = im.crop((bbox[0]-pad, bbox[1]-pad, bbox[2]+pad, bbox[3]+pad))
    crop.save(r"c:\Users\quinn\Desktop\AI PCB CAD\Q VFBMS32 AI PCB\scratch\crop_side_z25.png")
    print("Rendered and cropped crop_side_z25.png")
