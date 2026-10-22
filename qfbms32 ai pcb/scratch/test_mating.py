import subprocess
from PIL import Image

pcb_path = r"c:\Users\quinn\Desktop\AI PCB CAD\Q VFBMS32 AI PCB\VFBMS32.kicad_pcb"
kicad_cli = r"C:\Program Files\KiCad\10.0\bin\kicad-cli.exe"

# We want:
# 1. XT30PW-F mating face at X = 0
# 2. XT30PW-M mating face at X = 0, right side up

# Let's test varying the X offset for XT30PW-F
# and test rotations/offsets for XT30PW-M
tests = [
    # tag, f_rot, f_off, m_rot, m_off
    ("test1", "0 0 90", "0 2.2 0", "180 0 90", "0 3.2 0"),
    ("test2", "0 0 90", "0 2.6 0", "180 0 90", "0 3.8 0"),
    ("test3", "0 0 90", "0 2.2 0", "0 0 90", "0 3.2 0"),
    ("test4", "0 0 90", "0 2.2 0", "180 180 90", "0 3.2 0"),
]

for tag, f_rot, f_off, m_rot, m_off in tests:
    with open(pcb_path, "r", encoding="utf-8") as f:
        txt = f.read()

    import re
    # Update XT30PW-F
    idx_f = txt.find('(footprint "XT30PW-F_Lugs"')
    end_f = txt.find('(footprint "', idx_f + 10)
    sub_f = txt[idx_f:end_f]
    sub_f = re.sub(r'\(offset\s*\(xyz\s*[-0-9. ]+\)\s*\)', f'(offset (xyz {f_off}))', sub_f)
    sub_f = re.sub(r'\(rotate\s*\(xyz\s*[-0-9. ]+\)\s*\)', f'(rotate (xyz {f_rot}))', sub_f)
    txt = txt[:idx_f] + sub_f + txt[end_f:]

    # Update XT30PW-M
    idx_m = txt.find('(footprint "XT30PW-M_Lugs"')
    end_m = txt.find('(footprint "', idx_m + 10)
    sub_m = txt[idx_m:end_m]
    sub_m = re.sub(r'\(offset\s*\(xyz\s*[-0-9. ]+\)\s*\)', f'(offset (xyz {m_off}))', sub_m)
    sub_m = re.sub(r'\(rotate\s*\(xyz\s*[-0-9. ]+\)\s*\)', f'(rotate (xyz {m_rot}))', sub_m)
    txt = txt[:idx_m] + sub_m + txt[end_m:]

    with open(pcb_path, "w", encoding="utf-8") as f:
        f.write(txt)

    out_top = f"c:\\Users\\quinn\\Desktop\\AI PCB CAD\\test_mating_{tag}_top.png"
    subprocess.run([
        kicad_cli, "pcb", "render",
        "--side", "top",
        "--width", "1600", "--height", "600",
        "--background", "transparent",
        "-o", out_top, pcb_path
    ], check=True)

    im = Image.open(out_top)
    bbox = im.getbbox()
    if bbox:
        # crop left 450 pixels
        im.crop((bbox[0] - 20, bbox[1] - 20, bbox[0] + 350, bbox[3] + 20)).save(
            f"c:\\Users\\quinn\\Desktop\\AI PCB CAD\\crop_mating_{tag}.png"
        )
        print(f"Generated crop_mating_{tag}.png")

