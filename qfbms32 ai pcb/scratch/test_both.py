import subprocess, re
from PIL import Image

pcb_path = r'c:\Users\quinn\Desktop\AI PCB CAD\Q VFBMS32 AI PCB\VFBMS32.kicad_pcb'
kicad_cli = r'C:\Program Files\KiCad\10.0\bin\kicad-cli.exe'

# Both connectors: rot = (0, 0, 90)
# Test off_x for both so mating faces align with left edge (X = 0)
tests = [
    (3.5, 3.5),
    (3.8, 3.8),
    (4.0, 4.0),
    (4.2, 4.2),
]

for fx, mx in tests:
    with open(pcb_path, 'r', encoding='utf-8') as f:
        txt = f.read()

    # Replace XT30PW-F
    txt = re.sub(
        r'(\(footprint "XT30PW-F_Lugs".*?\(model "\$\{KIPRJMOD\}/3dmodels/XT30PW-F\.step"\s*\(offset\s*)\(xyz [^\)]+\)(\s*\)\s*\(scale\s*\(xyz 1 1 1\)\s*\)\s*\(rotate\s*)\(xyz [^\)]+\)',
        f'\\1(xyz {fx} 0 0)\\2(xyz 0 0 90)',
        txt,
        flags=re.DOTALL
    )

    # Replace XT30PW-M
    txt = re.sub(
        r'(\(footprint "XT30PW-M_Lugs".*?\(model "\$\{KIPRJMOD\}/3dmodels/XT30PW-M\.step"\s*\(offset\s*)\(xyz [^\)]+\)(\s*\)\s*\(scale\s*\(xyz 1 1 1\)\s*\)\s*\(rotate\s*)\(xyz [^\)]+\)',
        f'\\1(xyz {mx} 0 0)\\2(xyz 0 0 90)',
        txt,
        flags=re.DOTALL
    )

    with open(pcb_path, 'w', encoding='utf-8') as f:
        f.write(txt)

    out = f'c:\\Users\\quinn\\Desktop\\AI PCB CAD\\test_both_{fx}_{mx}.png'
    subprocess.run([kicad_cli, 'pcb', 'render', '--side', 'top', '--width', '1600', '--height', '600', '--background', 'transparent', '-o', out, pcb_path], check=True)
    im = Image.open(out)
    bbox = im.getbbox()
    im.crop((bbox[0]-20, bbox[1]-20, bbox[0]+350, bbox[3]+20)).save(f'c:\\Users\\quinn\\Desktop\\AI PCB CAD\\crop_both_{fx}_{mx}.png')

print("Done testing both!")
