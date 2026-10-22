with open("build_vfbms32_layout.py", "r", encoding="utf-8") as f:
    text = f.read()

import re
text = re.sub(
    r'\{\s*"dir":\s*[^,]+,\s*"lib":\s*[^,]+,\s*"fp":\s*"USB_C_Receptacle_16P"[\s\S]*?\},',
    """{
            "dir": custom_fp_dir,
            "lib": "",
            "fp": "USB_C_Receptacle_16P",
            "ref": "J_USB1",
            "val": "USB-C",
            "x": 125.0,
            "y": 3.2,
            "rot": 180.0
        },""",
    text
)

text = re.sub(
    r'\{\s*"dir":\s*[^,]+,\s*"lib":\s*[^,]+,\s*"fp":\s*"[^"]*"[\s\S]*?"ref":\s*"U7"[\s\S]*?\},',
    """{
            "dir": kicad_fp_dir,
            "lib": "Package_DIP.pretty",
            "fp": "SMDIP-8_W9.53mm",
            "ref": "U7",
            "val": "ISO1050 (DUB-8)",
            "x": 124.0,
            "y": 14.0,
            "rot": 0.0
        },""",
    text
)

with open("build_vfbms32_layout.py", "w", encoding="utf-8") as f:
    f.write(text)
print("Updated build_vfbms32_layout.py with locked DUB-8 at (124.0, 14.0, rot=0)!")
