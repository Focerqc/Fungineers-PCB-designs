import subprocess
from PIL import Image

pcb_path = r'c:\Users\quinn\Desktop\AI PCB CAD\Q VFBMS32 AI PCB\VFBMS32.kicad_pcb'
kicad_cli = r'C:\Program Files\KiCad\10.0\bin\kicad-cli.exe'

# Let's inspect the current render VFBMS32_layout_labeled.png and test_sw_crop.png
# Let's check what images already exist in project dir
import glob, os

imgs = glob.glob(r'c:\Users\quinn\Desktop\AI PCB CAD\Q VFBMS32 AI PCB\*.png')
for img in imgs:
    print(img, os.path.getsize(img))
