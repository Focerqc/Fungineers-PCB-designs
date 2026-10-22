import os

# Let's inspect build_vfbms32_layout.py
with open("build_vfbms32_layout.py", "r", encoding="utf-8") as f:
    code = f.read()

# Replace CH340N with ISO1050
code = code.replace('"val": "CH340N"', '"val": "ISO1050"')
code = code.replace('"fp": "SOIC-8_3.9x4.9mm_P1.27mm"', '"fp": "SOIC-8_7.5x5.85mm_P1.27mm"')

# Replace L2 if present
if '"ref": "L2"' in code:
    import re
    code = re.sub(r'\{\s*"dir":\s*[^,]+,\s*"lib":\s*[^,]+,\s*"fp":\s*"L_6.3x6.3_H3"[\s\S]*?\},', '', code)

with open("build_vfbms32_layout.py", "w", encoding="utf-8") as f:
    f.write(code)
print("Synchronized build_vfbms32_layout.py!")
