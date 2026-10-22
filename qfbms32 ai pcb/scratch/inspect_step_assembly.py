import re

path = r"c:\Users\quinn\Desktop\AI PCB CAD\Q VFBMS32 AI PCB\_reference\Meh ASM vbms STEP FILE.STEP"
with open(path, "r", errors="ignore") as f:
    text = f.read()

# find product definitions or component names
names = re.findall(r"PRODUCT\s*\(\s*'([^']+)'", text)
print("Products in STEP assembly:", set(names))

# find all occurrences of XT30 or related
for m in re.finditer(r"(XT30[^\n']*)", text, re.IGNORECASE):
    print("XT30 match:", m.group(1))

