import re

pcb_path = r"c:\Users\quinn\Documents\GitHub\Fungineers PCB designs\qfbms32 ai pcb\qfbms32.kicad_pcb"
sch_path = r"c:\Users\quinn\Documents\GitHub\Fungineers PCB designs\qfbms32 ai pcb\qfbms32.kicad_sch"

pcb = open(pcb_path, encoding="utf-8").read()
sch = open(sch_path, encoding="utf-8").read()


def parse_fps(text):
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
    out = []
    for b in blocks:
        mfp = re.search(r'\(footprint "([^"]+)"', b)
        mat = re.search(r"\(at ([-\d.]+) ([-\d.]+)(?: ([-\d.]+))?\)", b)
        mref = re.search(r'\(property "Reference" "([^"]+)"', b)
        mval = re.search(r'\(property "Value" "([^"]*)"', b)
        if mfp and mat and mref:
            out.append(
                {
                    "ref": mref.group(1),
                    "val": mval.group(1) if mval else "",
                    "fp": mfp.group(1),
                    "x": float(mat.group(1)),
                    "y": float(mat.group(2)),
                    "rot": mat.group(3) or "0",
                }
            )
    return out


fps = parse_fps(pcb)
print("=== All C_* and R_SSR* / nearby on PCB ===")
for f in sorted(fps, key=lambda t: t["ref"]):
    if f["ref"].startswith("C_") or "SSR" in f["ref"] or f["ref"] in (
        "R_G1",
        "R_GS1",
        "D_GS1",
        "R_SSR1",
    ):
        print(
            f"{f['ref']:10} {f['val']:14} at ({f['x']:.3f},{f['y']:.3f}) rot={f['rot']}  {f['fp']}"
        )

print("\n=== Schematic symbols of interest ===")
for m in re.finditer(r'\(property "Reference" "([^"]+)"', sch):
    ref = m.group(1)
    if any(
        x in ref
        for x in ["SSR", "G1", "GS1", "C_G", "C_GS", "C_SSR", "R_SSR", "R_G"]
    ):
        chunk = sch[m.start() : m.start() + 900]
        val = re.search(r'\(property "Value" "([^"]*)"', chunk)
        fp = re.search(r'\(property "Footprint" "([^"]*)"', chunk)
        at = re.search(r"\(at ([-\d.]+) ([-\d.]+)", sch[max(0, m.start() - 200) : m.start() + 50])
        # better: find enclosing symbol at
        print(
            f"{ref:10} val={val.group(1) if val else '?':12} fp={fp.group(1) if fp else '?'}"
        )

# Check empty pads / no footprint near box
print("\n=== Caps on board near y=3..8 x=26..34 ===")
for f in fps:
    if 26 <= f["x"] <= 34 and 3 <= f["y"] <= 8:
        print(f)
