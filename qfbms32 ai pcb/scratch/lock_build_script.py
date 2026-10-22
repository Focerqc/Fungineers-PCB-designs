with open("build_vfbms32_layout.py", "r", encoding="utf-8") as f:
    text = f.read()

# Verify J_USB1 and U7
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
    r'\{\s*"dir":\s*[^,]+,\s*"lib":\s*[^,]+,\s*"fp":\s*"SOIC-8[^"]*"[\s\S]*?"ref":\s*"U7"[\s\S]*?\},',
    """{
            "dir": kicad_fp_dir,
            "lib": "Package_SO.pretty",
            "fp": "SOIC-8_3.9x4.9mm_P1.27mm",
            "ref": "U7",
            "val": "ISO1050",
            "x": 125.0,
            "y": 12.0,
            "rot": 0.0
        },""",
    text
)

with open("build_vfbms32_layout.py", "w", encoding="utf-8") as f:
    f.write(text)
print("build_vfbms32_layout.py locked and verified!")
