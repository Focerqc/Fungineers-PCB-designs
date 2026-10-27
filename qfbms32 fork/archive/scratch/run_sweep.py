import subprocess, re
from PIL import Image

pcb_path = r'c:\Users\quinn\Desktop\AI PCB CAD\Q VFBMS32 AI PCB\VFBMS32.kicad_pcb'
kicad_cli = r'C:\Program Files\KiCad\10.0\bin\kicad-cli.exe'

# Let's test female with footprint at X = 5.2, Y = 7.45
# We test offset X from 4.0 to 6.0 in steps of 0.2
# And male with footprint at X = 4.0, Y = 24.55
# We test offset X from 3.5 to 4.5 in steps of 0.2

def render_test(f_fp_x, f_off_x, m_fp_x, m_off_x, tag):
    with open(pcb_path, 'r', encoding='utf-8') as f:
        txt = f.read()

    # Update J_CHG1 footprint pos
    txt = re.sub(
        r'(\(footprint "XT30PW-F_Lugs"[^\)]*\(at )([-\d.]+) ([-\d.]+)',
        f'\\g<1>{f_fp_x} 7.45',
        txt
    )
    # Update J_BAT1 footprint pos
    txt = re.sub(
        r'(\(footprint "XT30PW-M_Lugs"[^\)]*\(at )([-\d.]+) ([-\d.]+)',
        f'\\g<1>{m_fp_x} 24.55',
        txt
    )

    # Update female model offset
    # Note in kicad_pcb: (model "...XT30PW-F.step" (offset (xyz ...))
    txt = re.sub(
        r'(\(model "[^"]*XT30PW-F\.step"\s*\(offset\s*\(xyz\s*)[-\d.]+(\s+[-\d.]+\s+[-\d.]+\s*\))',
        f'\\g<1>{f_off_x} 0 0)',
        txt
    )

    # Update male model offset
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

    # Analyze crop
    w, h = crop.size
    # PCB left edge at Y=110 (middle between 7.45 and 24.55)
    pcb_x = None
    for x in range(w):
        r, g, b, a = crop.getpixel((x, int(h * 0.5)))
        if a > 100 and r < 100 and g > 50:
            pcb_x = x
            break

    # Female front edge (Y around 7.45mm -> h * 7.45/32)
    fy = int(h * (7.45 / 32.0))
    f_yellow_x = None
    for x in range(w):
        r, g, b, a = crop.getpixel((x, fy))
        if a > 100 and r > 150 and g > 150 and b < 100:
            f_yellow_x = x
            break

    # Male front edge (Y around 24.55mm -> h * 24.55/32)
    my = int(h * (24.55 / 32.0))
    m_yellow_x = None
    for x in range(w):
        r, g, b, a = crop.getpixel((x, my))
        if a > 100 and r > 150 and g > 150 and b < 100:
            m_yellow_x = x
            break

    scale = h / 32.0
    f_diff = (f_yellow_x - pcb_x) / scale if (f_yellow_x and pcb_x) else None
    m_diff = (m_yellow_x - pcb_x) / scale if (m_yellow_x and pcb_x) else None

    print(f"[{tag}] f_off={f_off_x}: f_diff={f_diff:+.3f}mm | m_off={m_off_x}: m_diff={m_diff:+.3f}mm (pcb_x={pcb_x}, f_x={f_yellow_x}, m_x={m_yellow_x})")

print("Running test sweep...")
for f_off in [5.0, 5.2, 5.4, 5.6, 5.8, 6.0]:
    render_test(f_fp_x=5.2, f_off_x=f_off, m_fp_x=4.0, m_off_x=4.1, tag=f"f_{f_off}")
