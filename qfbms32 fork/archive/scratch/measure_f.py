import subprocess, re
from PIL import Image

pcb_path = r'c:\Users\quinn\Desktop\AI PCB CAD\Q VFBMS32 AI PCB\VFBMS32.kicad_pcb'
kicad_cli = r'C:\Program Files\KiCad\10.0\bin\kicad-cli.exe'

for off_y in [2.8, 2.9, 3.0, 3.1]:
    with open(pcb_path, 'r', encoding='utf-8') as f:
        txt = f.read()

    idx_f = txt.find('(footprint "XT30PW-F_Lugs"')
    end_f = txt.find('(footprint "', idx_f + 10)
    sub_f = txt[idx_f:end_f]
    sub_f = re.sub(r'\(offset\s*\(xyz\s*[-0-9. ]+\)\s*\)', f'(offset (xyz 0 {off_y} 0))', sub_f)
    txt = txt[:idx_f] + sub_f + txt[end_f:]

    with open(pcb_path, 'w', encoding='utf-8') as f:
        f.write(txt)

    out = f'c:\\Users\\quinn\\Desktop\\AI PCB CAD\\test_f_off_{off_y}.png'
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
        r, g, b, a = im_c.getpixel((x, 40))
        if a > 100 and r > 150 and g > 150:
            cx = x
            break
    print(f'XT30PW-F off_y={off_y}: Board left={bx}, Conn left={cx}, Diff (Conn - Board)={cx - bx if bx is not None and cx is not None else None}')
