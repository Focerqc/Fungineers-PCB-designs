import re
import os

project_dir = r"c:\Users\quinn\Desktop\AI PCB CAD\Q VFBMS32 AI PCB"
vfbms_pretty = os.path.join(project_dir, "vfbms.pretty")

# 1. Update ESP32-C3-MINI-1.kicad_mod model path
esp_fp = os.path.join(vfbms_pretty, "ESP32-C3-MINI-1.kicad_mod")
with open(esp_fp, "r", encoding="utf-8") as f:
    text = f.read()

text = re.sub(r'\(model\s+"[^"]+"', '(model "${KIPRJMOD}/3dmodels/ESP32-C3-MINI-1.STEP"', text)
with open(esp_fp, "w", encoding="utf-8") as f:
    f.write(text)

print("Updated ESP32-C3-MINI-1.kicad_mod model path")

# 2. Create USB_C_Receptacle_16P.kicad_mod
src_fp = r"C:\Program Files\KiCad\10.0\share\kicad\footprints\Connector_USB.pretty\USB_C_Receptacle_GCT_USB4105-xx-A_16P_TopMnt_Horizontal.kicad_mod"
with open(src_fp, "r", encoding="utf-8") as f:
    usb_text = f.read()

usb_text = re.sub(r'\(model\s+"[^"]+"', '(model "${KIPRJMOD}/3dmodels/USB-C.step"', usb_text)
dst_fp = os.path.join(vfbms_pretty, "USB_C_Receptacle_16P.kicad_mod")
with open(dst_fp, "w", encoding="utf-8") as f:
    f.write(usb_text)

print("Created USB_C_Receptacle_16P.kicad_mod")
