import subprocess, re
from PIL import Image

pcb_path = r'c:\Users\quinn\Desktop\AI PCB CAD\Q VFBMS32 AI PCB\VFBMS32.kicad_pcb'
kicad_cli = r'C:\Program Files\KiCad\10.0\bin\kicad-cli.exe'

# Let's inspect the current VFBMS32.kicad_pcb render:
out = r'c:\Users\quinn\Desktop\AI PCB CAD\test_current.png'
subprocess.run([kicad_cli, 'pcb', 'render', '--side', 'top', '--width', '2400', '--height', '800', '--background', 'transparent', '-o', out, pcb_path], check=True)

im = Image.open(out)
bbox = im.getbbox()
print("Full render bbox:", bbox)

# Crop left 500 pixels around the connectors
crop = im.crop((bbox[0]-10, bbox[1]-10, bbox[0]+450, bbox[3]+10))
crop.save(r'c:\Users\quinn\Desktop\AI PCB CAD\test_crop.png')
print("Saved test_crop.png, size:", crop.size)
