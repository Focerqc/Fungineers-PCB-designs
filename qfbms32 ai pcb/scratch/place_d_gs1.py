"""Place D_GS1 (PDZ16B / ZL marking, SOD-323) at Box 1 center."""
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
fp_dir = r"C:\Program Files\KiCad\10.0\share\kicad\footprints\Diode_SMD.pretty"

bak_dir = os.path.join(pcb_dir, ".history")
os.makedirs(bak_dir, exist_ok=True)
shutil.copy2(pcb_path, os.path.join(bak_dir, "qfbms32_pre_d_gs1.kicad_pcb"))
shutil.copy2(sch_path, os.path.join(bak_dir, "qfbms32_pre_d_gs1.kicad_sch"))
print("Backed up PCB and schematic.")

# Box 1: 29.18, 10.85, 1.65x1.00 — Q1 gate-source zener (marking ZL = PDZ16B)
# Photo cathode silk on left, but photo is 180° vs CAD (R_GS1/474 sits above diode
# on board), so cathode is on board +X → rot=180.
part = {
    "ref": "D_GS1",
    "alt_refs": ["D_GS1", "D_TVS1", "D_G1", "D_BOX1"],
    "val": "PDZ16B",
    "fp_name": "D_SOD-323",
    "x": 29.18,
    "y": 10.85,
    "rot": 180.0,
    "desc": "Q1 gate-source 16V zener (ZL marking, SOD-323)",
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

# Schematic
with open(sch_path, "r", encoding="utf-8") as f:
    sch_text = f.read()

if part["ref"] not in sch_text:
    sch_add = f'''
	(symbol (lib_id "Device:D_Zener")
		(at 185.0 25.0 0)
		(unit 1)
		(exclude_from_sim no)
		(in_bom yes)
		(on_board yes)
		(dnp no)
		(uuid "{uuid.uuid4()}")
		(property "Reference" "{part["ref"]}" (at 185.0 21.0 0) (effects (font (size 1.27 1.27))))
		(property "Value" "{part["val"]}" (at 185.0 29.0 0) (effects (font (size 1.27 1.27))))
		(property "Footprint" "Diode_SMD:{part["fp_name"]}" (at 185.0 25.0 0) (hide yes) (effects (font (size 1.27 1.27))))
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

# boxes.json note
with open(boxes_path, "r", encoding="utf-8") as f:
    boxes_data = json.load(f)

for col in boxes_data.get("colors", []):
    if col.get("hex", "").lower() == "#4ea1ff":
        col["note"] = (
            "D_GS1 PDZ16B (ZL) 16V zener SOD-323 — Q1 G-S clamp; "
            "cathode toward +X (rot 180); close-up in chat / user_photos"
        )

for b in boxes_data.get("boxes", []):
    if abs(b.get("x", 0) - 29.175) < 0.02 and abs(b.get("y", 0) - 10.85) < 0.02:
        b["ref"] = part["ref"]
        b["val"] = part["val"]
        b["fpid"] = f"Diode_SMD:{part['fp_name']}"

with open(boxes_path, "w", encoding="utf-8") as f:
    json.dump(boxes_data, f, indent=1)
print("Updated qfbms32.boxes.json.")

# Render previews
raw_top_png = os.path.join(pcb_dir, "qfbms32_layout_top_hi_raw.png")
top_3d_png = os.path.join(pcb_dir, "qfbms32_3d_top.png")
iso_3d_png = os.path.join(pcb_dir, "qfbms32_3d_iso.png")

print("Rendering top 3D...")
subprocess.run(
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
subprocess.run(
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
import generate_annotated_preview

generate_annotated_preview.generate_annotated_preview()
print("Done.")
