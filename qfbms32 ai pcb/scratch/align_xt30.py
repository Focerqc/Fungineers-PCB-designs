import re
import subprocess
from PIL import Image

pcb_path = r"c:\Users\quinn\Desktop\AI PCB CAD\Q VFBMS32 AI PCB\VFBMS32.kicad_pcb"
kicad_cli = r"C:\Program Files\KiCad\10.0\bin\kicad-cli.exe"

def update_model(board_text, step_name, off_xyz, rot_xyz):
    # Regex for model inside footprint
    # Matches:
    # (model "${KIPRJMOD}/3dmodels/XT30PW-F.step"
    #   (offset (xyz 0 0 0))
    #   (scale (xyz 1 1 1))
    #   (rotate (xyz 0 0 0))
    # )
    pattern = re.compile(
        r'(\(model "\$\{KIPRJMOD\}/3dmodels/' + re.escape(step_name) + r'"\s*'
        r'\(offset\s*\(\s*xyz\s*)[^\)]+(\)\s*\)\s*'
        r'\(scale\s*\(\s*xyz\s*)[^\)]+(\)\s*\)\s*'
        r'\(rotate\s*\(\s*xyz\s*)[^\)]+(\)\s*\)\s*\)',
        re.DOTALL
    )
    replacement = r'\g<1>' + off_xyz + r'\g<2>1 1 1\g<3>' + rot_xyz + r'))'
    
    # If the previous buggy regex stripped the closing brackets, let's fix it cleanly
    new_text, n = pattern.subn(replacement, board_text)
    return new_text

def test_config(f_rot, f_off, m_rot, m_off, tag="test"):
    with open(pcb_path, "r", encoding="utf-8") as f:
        txt = f.read()

    # Normalize any damaged model closing block for XT30PW-F and XT30PW-M
    txt = re.sub(
        r'(\(model "\$\{KIPRJMOD\}/3dmodels/XT30PW-[FM]\.step".*?\(rotate\s*\(xyz\s*)[^\)]+(\)\s*).*?(\t\(footprint)',
        r'\1 0 0 0\n\t\t\t)\n\t\t)\n\t)\n\3',
        txt,
        flags=re.DOTALL
    )

    txt = update_model(txt, "XT30PW-F.step", f_off, f_rot)
    txt = update_model(txt, "XT30PW-M.step", m_off, m_rot)

    with open(pcb_path, "w", encoding="utf-8") as f:
        f.write(txt)

    out_png = f"align_{tag}.png"
    subprocess.run([
        kicad_cli, "pcb", "render",
        "--side", "top",
        "--width", "2400", "--height", "800",
        "--background", "transparent",
        "-o", out_png, pcb_path
    ], check=True)

    im = Image.open(out_png)
    bbox = im.getbbox()
    if bbox:
        crop = im.crop((bbox[0], bbox[1], bbox[0] + 450, bbox[3]))
        crop.save(f"align_{tag}_zoom.png")
        print(f"Saved align_{tag}_zoom.png successfully!")

if __name__ == "__main__":
    test_config("0 0 90", "0 0 0", "0 0 90", "0 0 0", tag="rot90")
