import re
import os
import subprocess
from PIL import Image

project_dir = r"c:\Users\quinn\Desktop\AI PCB CAD\Q VFBMS32 AI PCB"
pcb_path = os.path.join(project_dir, "VFBMS32.kicad_pcb")

with open(pcb_path, "r", encoding="utf-8") as f:
    text = f.read()

# Update U_ESP1 model
old_esp_model = r'\(model\s+\"\$\{KICAD10_3DMODEL_DIR\}/RF_Module\.3dshapes/ESP32-C6-MINI-1\.step\"[\s\S]*?\n\t\t\)'
new_esp_model = '''(model "${KIPRJMOD}/3dmodels/ESP32-C3-MINI-1.STEP"
\t\t\t(offset
\t\t\t\t(xyz -6.6 -8.37 0)
\t\t\t)
\t\t\t(scale
\t\t\t\t(xyz 1 1 1)
\t\t\t)
\t\t\t(rotate
\t\t\t\t(xyz 0 0 0)
\t\t\t)
\t\t)'''

# Update J_USB1 model
old_usb_model = r'\(model\s+\"\$\{KICAD10_3DMODEL_DIR\}/Connector_USB\.3dshapes/USB_C_Receptacle_HRO_TYPE-C-31-M-12\.step\"[\s\S]*?\n\t\t\)'
new_usb_model = '''(model "${KIPRJMOD}/3dmodels/USB-C.step"
\t\t\t(offset
\t\t\t\t(xyz 0 0 0)
\t\t\t)
\t\t\t(scale
\t\t\t\t(xyz 1 1 1)
\t\t\t)
\t\t\t(rotate
\t\t\t\t(xyz 0 0 0)
\t\t\t)
\t\t)'''

text = re.sub(old_esp_model, new_esp_model, text)
text = re.sub(old_usb_model, new_usb_model, text)

with open(pcb_path, "w", encoding="utf-8") as f:
    f.write(text)

print("Updated VFBMS32.kicad_pcb models")

# Now render 3D view
kicad_cli = r"C:\Program Files\KiCad\10.0\bin\kicad-cli.exe"
test_png = os.path.join(project_dir, "scratch", "test_render_esp_usb.png")

res = subprocess.run([
    kicad_cli, "pcb", "render",
    "--perspective",
    "--rotate", "-25,0,25",
    "--floor",
    "--width", "3600", "--height", "1600",
    "--background", "transparent",
    "-o", test_png, pcb_path
], capture_output=True, text=True)

print("Render return code:", res.returncode)
if res.stderr:
    print("Render stderr:", res.stderr[:300])

if os.path.exists(test_png):
    im = Image.open(test_png)
    bbox = im.getbbox()
    if bbox:
        pad = 40
        box = (max(0, bbox[0]-pad), max(0, bbox[1]-pad), min(im.width, bbox[2]+pad), min(im.height, bbox[3]+pad))
        im.crop(box).save(test_png)
        print(f"Saved test render: {test_png}, size={im.size}")
