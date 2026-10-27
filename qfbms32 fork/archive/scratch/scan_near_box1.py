import re

path = r"c:\Users\quinn\Documents\GitHub\Fungineers PCB designs\qfbms32 ai pcb\qfbms32.kicad_pcb"
text = open(path, encoding="utf-8").read()

blocks = []
i = 0
while True:
    start = text.find("(footprint ", i)
    if start < 0:
        break
    depth = 0
    j = start
    while j < len(text):
        if text[j] == "(":
            depth += 1
        elif text[j] == ")":
            depth -= 1
            if depth == 0:
                j += 1
                break
        j += 1
    blocks.append(text[start:j])
    i = j

hits = []
for b in blocks:
    mfp = re.search(r'\(footprint "([^"]+)"', b)
    mat = re.search(r"\(at ([-\d.]+) ([-\d.]+)(?: ([-\d.]+))?\)", b)
    mref = re.search(r'\(property "Reference" "([^"]+)"', b)
    mval = re.search(r'\(property "Value" "([^"]*)"', b)
    if not (mfp and mat and mref):
        continue
    fp = mfp.group(1)
    x, y = float(mat.group(1)), float(mat.group(2))
    rot = mat.group(3) or "0"
    ref = mref.group(1)
    val = mval.group(1) if mval else ""
    if 24 <= x <= 36 and 2 <= y <= 14:
        hits.append((x, y, rot, ref, val, fp))

hits.sort(key=lambda t: (t[1], t[0]))
print("=== Near Box1 (24-36 x, 2-14 y) target=(29.15,5.70) ===")
for h in hits:
    mark = " <<<" if abs(h[0] - 29.15) < 2 and abs(h[1] - 5.70) < 1.5 else ""
    print(f"{h[3]:10} {h[4]:14} at ({h[0]:.3f},{h[1]:.3f}) rot={h[2]}  {h[5]}{mark}")
