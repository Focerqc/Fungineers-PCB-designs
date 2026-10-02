import subprocess
import re
from PIL import Image

project_dir = r"c:\Users\quinn\Desktop\AI PCB CAD\Q VFBMS32 AI PCB"
kicad_fp_dir = r"C:\Program Files\KiCad\10.0\share\kicad\footprints"
custom_fp_dir = r"c:\Users\quinn\Desktop\AI PCB CAD\Q VFBMS32 AI PCB\vfbms.pretty"
pcb_path = r"c:\Users\quinn\Desktop\AI PCB CAD\Q VFBMS32 AI PCB\VFBMS32.kicad_pcb"
kicad_cli = r"C:\Program Files\KiCad\10.0\bin\kicad-cli.exe"

# 1. Update create_xt30_footprints.py
# In SolidWorks:
# XT30PW-F (Female):
# mating face is at -X relative to board edge.
# We want mating face of XT30PW-F and XT30PW-M to be at X = 0.0 when placed on board.
# Let's test offsets in footprint file directly:
def test(f_fp_x, f_off_x, m_fp_x, m_off_x):
    # Footprint files:
    fp_f_file = rf"{custom_fp_dir}\XT30PW-F_Lugs.kicad_mod"
    fp_m_file = rf"{custom_fp_dir}\XT30PW-M_Lugs.kicad_mod"

    with open(fp_f_file, "r") as f:
        tf = f.read()
    tf = re.sub(r'\(offset\s*\(xyz\s*[-0-9. ]+\)\s*\)', f'(offset (xyz {f_off_x} 0 0))', tf)
    tf = re.sub(r'\(rotate\s*\(xyz\s*[-0-9. ]+\)\s*\)', '(rotate (xyz 0 0 90))', tf)
    with open(fp_f_file, "w") as f:
        f.write(tf)

    with open(fp_m_file, "r") as f:
        tm = f.read()
    tm = re.sub(r'\(offset\s*\(xyz\s*[-0-9. ]+\)\s*\)', f'(offset (xyz {m_off_x} 0 0))', tm)
    tm = re.sub(r'\(rotate\s*\(xyz\s*[-0-9. ]+\)\s*\)', '(rotate (xyz 0 0 90))', tm)
    with open(fp_m_file, "w") as f:
        f.write(tm)

    # Now run build_vfbms32_layout with J_CHG1 at (f_fp_x, 7.45) and J_BAT1 at (m_fp_x, 24.55)
    layout_py = rf"{project_dir}\build_vfbms32_layout.py"
    with open(layout_py, "r") as f:
        tl = f.read()
    # update J_CHG1 x, y
    tl = re.sub(r'("ref":\s*"J_CHG1",.*?"x":\s*)[-\d.]+(,.*?"y":\s*)[-\d.]+', f'\\g<1>{f_fp_x}\\g<2>7.45', tl, flags=re.DOTALL)
    # update J_BAT1 x, y
    tl = re.sub(r'("ref":\s*"J_BAT1",.*?"x":\s*)[-\d.]+(,.*?"y":\s*)[-\d.]+', f'\\g<1>{m_fp_x}\\g<2>24.55', tl, flags=re.DOTALL)
    with open(layout_py, "w") as f:
        f.write(tl)

    # Run build layout
    subprocess.run([r"C:\Program Files\KiCad\10.0\bin\python.exe", layout_py], check=True)

    # Render
    out_img = rf"{project_dir}\test_solidworks_match.png"
    subprocess.run([kicad_cli, "pcb", "render", "--side", "top", "--width", "1800", "--height", "600", "--background", "transparent", "-o", out_img, pcb_path], check=True)

    im = Image.open(out_img)
    bbox = im.getbbox()
    crop = im.crop((bbox[0]-20, bbox[1]-20, bbox[0]+400, bbox[3]+20))
    crop.save(rf"{project_dir}\test_sw_crop.png")
    print("Rendered test_sw_crop.png")

if __name__ == "__main__":
    # In SolidWorks:
    # F footprint at X ~ 6.0, offset 6.0
    # M footprint at X ~ 4.5, offset 4.5
    test(f_fp_x=6.0, f_off_x=6.0, m_fp_x=4.5, m_off_x=4.5)
