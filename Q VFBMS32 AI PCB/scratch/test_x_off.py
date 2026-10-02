import subprocess
import re
from PIL import Image

pcb_path = r'c:\Users\quinn\Desktop\AI PCB CAD\Q VFBMS32 AI PCB\VFBMS32.kicad_pcb'
kicad_cli = r'C:\Program Files\KiCad\10.0\bin\kicad-cli.exe'

with open(pcb_path, 'r', encoding='utf-8') as f:
    txt = f.read()

# XT30PW-F: test X offsets 1.5, 2.0, 2.5
for off_x in [1.5, 2.0, 2.5]:
    txt_new = re.sub(
        r'(\(footprint "XT30PW-F_Lugs".*?\(model "\$\{KIPRJMOD\}/3dmodels/XT30PW-F\.step"\s*\(offset\s*)\(xyz [^\)]+\)',
        f'\\1(xyz {off_x} 0 0)',
        txt,
        flags=re.DOTALL
    )
    with open(pcb_path, 'w', encoding='utf-8') as f:
        f.write(txt_new)
    
    out = f'c:\\Users\\quinn\\Desktop\\AI PCB CAD\\test_fx_{off_x}.png'
    subprocess.run([kicad_cli, 'pcb', 'render', '--side', 'top', '--width', '1600', '--height', '600', '--background', 'transparent', '-o', out, pcb_path], check=True)
    im = Image.open(out)
    bbox = im.getbbox()
    im.crop((bbox[0]-20, bbox[1]-20, bbox[0]+350, bbox[3]+20)).save(f'c:\\Users\\quinn\\Desktop\\AI PCB CAD\\crop_fx_{off_x}.png')
    print('Done', off_x)
