import subprocess, re
from PIL import Image

pcb_path = r'c:\Users\quinn\Desktop\AI PCB CAD\Q VFBMS32 AI PCB\VFBMS32.kicad_pcb'
kicad_cli = r'C:\Program Files\KiCad\10.0\bin\kicad-cli.exe'

# Let's test female off_x: 5.4, 5.6, 5.8, 6.0
# with female Y = 7.45, male Y = 24.55
for fx in [5.4, 5.6, 5.8, 6.0]:
    with open(pcb_path, 'r', encoding='utf-8') as f:
        txt = f.read()

    # Update J_CHG1 position (at 5.2 7.45)
    txt = re.sub(
        r'(\(footprint "XT30PW-F_Lugs"[^\)]*\(at )([-\d.]+) ([-\d.]+)',
        r'\g<1>5.2 7.45',
        txt
    )
    # Update J_BAT1 position (at 4.0 24.55)
    txt = re.sub(
        r'(\(footprint "XT30PW-M_Lugs"[^\)]*\(at )([-\d.]+) ([-\d.]+)',
        r'\g<1>4.0 24.55',
        txt
    )

    # Replace XT30PW-F offset
    txt = re.sub(
        r'(\(footprint "XT30PW-F_Lugs".*?\(model "\$\{KIPRJMOD\}/3dmodels/XT30PW-F\.step"\s*\(offset\s*)\(xyz [^\)]+\)(\s*\)\s*\(scale\s*\(xyz 1 1 1\)\s*\)\s*\(rotate\s*)\(xyz [^\)]+\)',
        f'\\1(xyz {fx} 0 0)\\2(xyz 0 0 90)',
        txt,
        flags=re.DOTALL
    )

    # Replace XT30PW-M offset (keep mx=4.1, rot=0 0 90)
    txt = re.sub(
        r'(\(footprint "XT30PW-M_Lugs".*?\(model "\$\{KIPRJMOD\}/3dmodels/XT30PW-M\.step"\s*\(offset\s*)\(xyz [^\)]+\)(\s*\)\s*\(scale\s*\(xyz 1 1 1\)\s*\)\s*\(rotate\s*)\(xyz [^\)]+\)',
        r'\1(xyz 4.1 0 0)\2(xyz 0 0 90)',
        txt,
        flags=re.DOTALL
    )

    with open(pcb_path, 'w', encoding='utf-8') as f:
        f.write(txt)

    out = f'c:\\Users\\quinn\\Desktop\\AI PCB CAD\\test_exact_f_{fx}.png'
    subprocess.run([kicad_cli, 'pcb', 'render', '--side', 'top', '--width', '1600', '--height', '600', '--background', 'transparent', '-o', out, pcb_path], check=True)
    im = Image.open(out)
    bbox = im.getbbox()
    im_c = im.crop((bbox[0]-20, bbox[1]-20, bbox[0]+350, bbox[3]+20))
    im_c.save(f'c:\\Users\\quinn\\Desktop\\AI PCB CAD\\crop_exact_f_{fx}.png')

    # Measure
    bx = None
    for x in range(im_c.width):
        r, g, b, a = im_c.getpixel((x, 100))
        if a > 100 and g > 30 and g > r:
            bx = x
            break
    cx_f = None
    for x in range(im_c.width):
        r, g, b, a = im_c.getpixel((x, 40))
        if a > 100 and r > 150 and g > 150:
            cx_f = x
            break
    cx_m = None
    for x in range(im_c.width):
        r, g, b, a = im_c.getpixel((x, 150))
        if a > 100 and r > 150 and g > 150:
            cx_m = x
            break
    print(f'fx={fx}: Board left={bx}, Top conn={cx_f} (diff={cx_f-bx if bx and cx_f else None}), Bot conn={cx_m} (diff={cx_m-bx if bx and cx_m else None})')
