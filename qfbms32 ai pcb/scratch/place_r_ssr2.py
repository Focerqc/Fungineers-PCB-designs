"""Place R_SSR2 (10k, 0603) at Box 1 — unmarked part measured ~9.97k on CM300 60k range."""
import json
import os
import shutil
import subprocess
import uuid

import pcbnew
from PIL import Image

pcb_dir = r"c:\Users\quinn\Documents\GitHub\Fungineers PCB designs\qfbms32 ai pcb"
pcb_path = os.path.join(pcb_dir, "qfbms32.kicad_pcb")
sch_path = os.path.join(pcb_dir, "qfbms32.kicad_sch")
boxes_path = os.path.join(pcb_dir, "qfbms32.boxes.json")
kicad_cli = r"C:\Program Files\KiCad\10.0\bin\kicad-cli.exe"
fp_dir = r"C:\Program Files\KiCad\10.0\share\kicad\footprints\Resistor_SMD.pretty"

bak_dir = os.path.join(pcb_dir, ".history")
os.makedirs(bak_dir, exist_ok=True)
shutil.copy2(pcb_path, os.path.join(bak_dir, "qfbms32_pre_r_ssr2.kicad_pcb"))
shutil.copy2(sch_path, os.path.join(bak_dir, "qfbms32_pre_r_ssr2.kicad_sch"))
print("Backed up PCB and schematic.")

# Box 1: 29.15, 5.70, 1.75x0.95 — between R_SSR1 and R_G1; meter 9.97 on 60k = ~10k
part = {
    "ref": "R_SSR2",
    "alt_refs": ["R_SSR2", "R_BOX1", "R_G0", "R_PD1"],
    "val": "10k",
    "fp_name": "R_0603_1608Metric",
    "x": 29.15,
    "y": 5.70,
    "rot": 0.0,
    "desc": "Unmarked 0603; CM300 60k range read 9.97 (~10k); between R_SSR1 and R_G1",
}

board = pcbnew.LoadBoard(pcb_path)
for r in part["alt_refs"]:
    fp = board.FindFootprintByReference(r)
    if fp:
        print(f"Removing existing {r}")
        board.Remove(fp)

fp = pcbnew.FootprintLoad(fp_dir, part["fp_name"])
if not fp:
    raise RuntimeError(f"Failed to load {part['fp_name']}")
board.Add(fp)
fp.SetReference(part["ref"])
fp.SetValue(part["val"])
fp.SetPosition(pcbnew.VECTOR2I(pcbnew.FromMM(part["x"]), pcbnew.FromMM(part["y"])))
fp.SetOrientation(pcbnew.EDA_ANGLE(part["rot"], pcbnew.DEGREES_T))
fp.Reference().SetVisible(False)
fp.Value().SetVisible(False)
pcbnew.SaveBoard(pcb_path, board)
print(
    f"Placed {part['ref']} ({part['val']}) {part['fp_name']} "
    f"at ({part['x']}, {part['y']}) rot={part['rot']}° — {part['desc']}"
)

with open(sch_path, "r", encoding="utf-8") as f:
    sch_text = f.read()

if part["ref"] not in sch_text:
    sch_add = f'''
	(symbol (lib_id "Device:R")
		(at 185.0 35.0 0)
		(unit 1)
		(exclude_from_sim no)
		(in_bom yes)
		(on_board yes)
		(dnp no)
		(uuid "{uuid.uuid4()}")
		(property "Reference" "{part["ref"]}" (at 185.0 31.0 0) (effects (font (size 1.27 1.27))))
		(property "Value" "{part["val"]}" (at 185.0 39.0 0) (effects (font (size 1.27 1.27))))
		(property "Footprint" "Resistor_SMD:{part["fp_name"]}" (at 185.0 35.0 0) (hide yes) (effects (font (size 1.27 1.27))))
		(pin "1" (uuid "{uuid.uuid4()}"))
		(pin "2" (uuid "{uuid.uuid4()}"))
		(instances
			(project "qfbms32"
				(path "/a2322edc-ff52-449c-92df-24faffac0236" (reference "{part["ref"]}") (unit 1))
			)
		)
	)
'''
    insert_pos = sch_text.rfind("(sheet_instances")
    if insert_pos == -1:
        raise RuntimeError("sheet_instances not found in schematic")
    sch_text = sch_text[:insert_pos] + sch_add + "\n\t" + sch_text[insert_pos:]
    with open(sch_path, "w", encoding="utf-8") as f:
        f.write(sch_text)
    print(f"Added {part['ref']} to schematic.")
else:
    print(f"{part['ref']} already in schematic.")

with open(boxes_path, "r", encoding="utf-8") as f:
    boxes_data = json.load(f)

for col in boxes_data.get("colors", []):
    if col.get("hex", "").lower() == "#4ea1ff":
        col["note"] = (
            "R_SSR2 10k 0603 — unmarked; CM300 60k read 9.97 (~10k); "
            "between R_SSR1 and R_G1 at (29.15, 5.70)"
        )

for b in boxes_data.get("boxes", []):
    if abs(b.get("x", 0) - 29.15) < 0.05 and abs(b.get("y", 0) - 5.70) < 0.05:
        b["ref"] = part["ref"]
        b["val"] = part["val"]
        b["fpid"] = f"Resistor_SMD:{part['fp_name']}"

with open(boxes_path, "w", encoding="utf-8") as f:
    json.dump(boxes_data, f, indent=1)
print("Updated qfbms32.boxes.json.")

# Update meter reference note
md_path = os.path.join(pcb_dir, "_reference", "tools", "centech_cm300.md")
if os.path.exists(md_path):
    with open(md_path, "r", encoding="utf-8") as f:
        md = f.read()
    old = (
        "Unmarked dark 0603 between `R_SSR1` (01X) and `R_G1` (01X) at ~**(29.15, 5.70)** mm "
        "on `qfbms32` — Box 1, color note “unmarked idk”. Most likely MLCC or ferrite bead pending meter check."
    )
    new = (
        "Box 1 at **(29.15, 5.70)** — measured **9.97 on 60k Ω ≈ 10 kΩ**. "
        "Placed as `R_SSR2` 10k 0603 (was unmarked; broke off during probe)."
    )
    if old in md:
        md = md.replace(old, new)
        with open(md_path, "w", encoding="utf-8") as f:
            f.write(md)
        print("Updated centech_cm300.md")

raw_top_png = os.path.join(pcb_dir, "qfbms32_layout_top_hi_raw.png")
top_3d_png = os.path.join(pcb_dir, "qfbms32_3d_top.png")
iso_3d_png = os.path.join(pcb_dir, "qfbms32_3d_iso.png")

print("Rendering top 3D...")
r1 = subprocess.run(
    [
        kicad_cli, "pcb", "render",
        "--side", "top",
        "--width", "4000", "--height", "2000",
        "--background", "transparent",
        "-o", raw_top_png, pcb_path,
    ],
    capture_output=True,
    text=True,
)
if r1.returncode != 0:
    print("top render stderr:", r1.stderr[-500:] if r1.stderr else r1.stdout[-500:])
if os.path.exists(raw_top_png):
    im = Image.open(raw_top_png)
    bbox = im.getbbox()
    if bbox:
        pad = 30
        crop_box = (
            max(0, bbox[0] - pad),
            max(0, bbox[1] - pad),
            min(im.width, bbox[2] + pad),
            min(im.height, bbox[3] + pad),
        )
        im.crop(crop_box).save(top_3d_png)
        print(f"Saved {top_3d_png}")

print("Rendering iso 3D...")
r2 = subprocess.run(
    [
        kicad_cli, "pcb", "render",
        "--rotate", "-45,0,45",
        "--width", "4000", "--height", "2600",
        "--background", "transparent",
        "-o", iso_3d_png, pcb_path,
    ],
    capture_output=True,
    text=True,
)
if r2.returncode != 0:
    print("iso render stderr:", r2.stderr[-500:] if r2.stderr else r2.stdout[-500:])
if os.path.exists(iso_3d_png):
    im = Image.open(iso_3d_png)
    bbox = im.getbbox()
    if bbox:
        pad = 20
        crop_box = (
            max(0, bbox[0] - pad),
            max(0, bbox[1] - pad),
            min(im.width, bbox[2] + pad),
            min(im.height, bbox[3] + pad),
        )
        im.crop(crop_box).save(iso_3d_png)
        print(f"Saved {iso_3d_png}")

import sys

sys.path.insert(0, pcb_dir)
try:
    import generate_annotated_preview

    generate_annotated_preview.generate_annotated_preview()
except Exception as e:
    print(f"Annotated preview skipped: {e}")
print("Done.")
