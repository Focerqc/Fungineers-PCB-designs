import subprocess, re
from PIL import Image

pcb_path = r'c:\Users\quinn\Desktop\AI PCB CAD\Q VFBMS32 AI PCB\VFBMS32.kicad_pcb'
kicad_cli = r'C:\Program Files\KiCad\10.0\bin\kicad-cli.exe'

for off_y in [3.0, 3.5, 4.0, 4.5]:
    with open(pcb_path, 'r', encoding='utf-8') as f:
        txt = f.read()

    idx_m = txt.find('(footprint "XT30PW-M_Lugs"')
    end_m = txt.find('(footprint "', idx_m + 10)
    sub_m = txt[idx_m:end_m]
    sub_m = re.sub(r'\(offset\s*\(xyz\s*[-0-9. ]+\)\s*\)', f'(offset (xyz 0 {off_y} 0))', sub_m)
    sub_m = re.sub(r'\(rotate\s*\(xyz\s*[-0-9. ]+\)\s*\)', '(rotate (xyz 0 0 90))', sub_m)
    txt = txt[:idx_m] + sub_m + txt[end_m:]

    with open(pcb_path, 'w', encoding='utf-8') as f:
        f.write(txt)

    out = f'c:\\Users\\quinn\\Desktop\\AI PCB CAD\\test_m_off_{off_y}.png'
    subprocess.run([kicad_cli, 'pcb', 'render', '--side', 'top', '--width', '1600', '--height', '600', '--background', 'transparent', '-o', out, pcb_path], check=True)
    im = Image.open(out)
    bbox = im.getbbox()
    im_c = im.crop((bbox[0]-20, bbox[1]-20, bbox[0]+350, bbox[3]+20))
    bx = None
    for x in range(im_c.width):
        r, g, b, a = im_c.getpixel((x, 100))
        if a > 100 and g > 30 and g > r:
            bx = x
            break
    cx = None
    for x in range(im_c.width):
        r, g, b, a = im_c.getpixel((x, 160))
        if a > 100 and r > 150 and g > 150:
            cx = x
            break
    print(f'off_y={off_y}: Board left={bx}, Conn left={cx}, Diff (Conn - Board)={cx - bx if bx is not None and cx is not None else None}')
