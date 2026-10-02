import subprocess, re
from PIL import Image

pcb_path = r'c:\Users\quinn\Desktop\AI PCB CAD\Q VFBMS32 AI PCB\VFBMS32.kicad_pcb'
kicad_cli = r'C:\Program Files\KiCad\10.0\bin\kicad-cli.exe'

def render_test(f_fp_x, f_off_x, m_fp_x, m_off_x, tag):
    with open(pcb_path, 'r', encoding='utf-8') as f:
        txt = f.read()

    txt = re.sub(
        r'(\(footprint "XT30PW-F_Lugs"[^\)]*\(at )([-\d.]+) ([-\d.]+)',
        f'\\g<1>{f_fp_x} 7.45',
        txt
    )
    txt = re.sub(
        r'(\(footprint "XT30PW-M_Lugs"[^\)]*\(at )([-\d.]+) ([-\d.]+)',
        f'\\g<1>{m_fp_x} 24.55',
        txt
    )
    txt = re.sub(
        r'(\(model "[^"]*XT30PW-F\.step"\s*\(offset\s*\(xyz\s*)[-\d.]+(\s+[-\d.]+\s+[-\d.]+\s*\))',
        f'\\g<1>{f_off_x} 0 0)',
        txt
    )
    txt = re.sub(
        r'(\(model "[^"]*XT30PW-M\.step"\s*\(offset\s*\(xyz\s*)[-\d.]+(\s+[-\d.]+\s+[-\d.]+\s*\))',
        f'\\g<1>{m_off_x} 0 0)',
        txt
    )

    with open(pcb_path, 'w', encoding='utf-8') as f:
        f.write(txt)

    out_png = rf'c:\Users\quinn\Desktop\AI PCB CAD\test_align_{tag}.png'
    subprocess.run([
        kicad_cli, 'pcb', 'render',
        '--side', 'top',
        '--width', '2400', '--height', '800',
        '--background', 'transparent',
        '-o', out_png, pcb_path
    ], check=True)

    im = Image.open(out_png)
    bbox = im.getbbox()
    crop = im.crop((bbox[0]-10, bbox[1]-10, bbox[0]+450, bbox[3]+10))
    crop.save(rf'c:\Users\quinn\Desktop\AI PCB CAD\crop_{tag}.png')

    w, h = crop.size
    pcb_x = None
    for x in range(w):
        r, g, b, a = crop.getpixel((x, int(h * 0.5)))
        if a > 100 and r < 100 and g > 50:
            pcb_x = x
            break

    # Check across female connector Y range (fy from 0.15*h to 0.35*h)
    f_yellow_min_x = 999
    for y in range(int(h * 0.15), int(h * 0.32)):
        for x in range(w):
            r, g, b, a = crop.getpixel((x, y))
            if a > 100 and r > 150 and g > 150 and b < 100:
                if x < f_yellow_min_x:
                    f_yellow_min_x = x
                break

    scale = h / 32.0
    f_diff = (f_yellow_min_x - pcb_x) / scale if (f_yellow_min_x < 999 and pcb_x) else None
    print(f"[{tag}] f_off={f_off_x}: pcb_x={pcb_x}, f_min_x={f_yellow_min_x}, f_diff={f_diff:+.3f}mm")

for f_off in [0.0, 0.5, 0.8, 1.0, 1.2, 1.5, 2.0]:
    render_test(f_fp_x=5.2, f_off_x=f_off, m_fp_x=4.0, m_off_x=4.1, tag=f"f_{f_off}")
