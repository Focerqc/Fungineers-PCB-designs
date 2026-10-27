import pcbnew
import os
import shutil
import subprocess
import json
import uuid
import re
from PIL import Image

pcb_dir = r"c:\Users\quinn\Documents\GitHub\Fungineers PCB designs\qfbms32 ai pcb"
pcb_path = os.path.join(pcb_dir, "qfbms32.kicad_pcb")
sch_path = os.path.join(pcb_dir, "qfbms32.kicad_sch")
boxes_path = os.path.join(pcb_dir, "qfbms32.boxes.json")
kicad_cli = r"C:\Program Files\KiCad\10.0\bin\kicad-cli.exe"
brain_dir = r"C:\Users\quinn\.gemini\antigravity-ide\brain\81dccd88-dad8-4422-8970-0c1c2920cd0b"
os.makedirs(brain_dir, exist_ok=True)

# 1. Backup PCB and Schematic
bak_dir = os.path.join(pcb_dir, ".history")
os.makedirs(bak_dir, exist_ok=True)
shutil.copy2(pcb_path, os.path.join(bak_dir, "qfbms32_pre_two_caps.kicad_pcb"))
shutil.copy2(sch_path, os.path.join(bak_dir, "qfbms32_pre_two_caps.kicad_sch"))
print("Backed up PCB and schematic.")

# 2. Update KiCad PCB with C_SSR1 and C_SSR2
board = pcbnew.LoadBoard(pcb_path)
kicad_fp_dir = r"C:\Program Files\KiCad\10.0\share\kicad\footprints\Capacitor_SMD.pretty"

caps = [
    {
        "ref": "C_SSR1",
        "alt_refs": ["C_SSR1", "C_TOP1", "C_CHG1"],
        "val": "100nF",
        "desc": "SSR / Charge stage snubber/filter capacitor (Color 1 Box 1, lighter tan)",
        "fp_lib": kicad_fp_dir,
        "fp_name": "C_0603_1608Metric",
        "x": 28.45,
        "y": 1.75,
        "rot": 90.0
    },
    {
        "ref": "C_SSR2",
        "alt_refs": ["C_SSR2", "C_TOP2", "C_CHG2"],
        "val": "1uF",
        "desc": "SSR / Charge stage high-voltage bulk capacitor (Color 2 Box 1, darker orange)",
        "fp_lib": kicad_fp_dir,
        "fp_name": "C_0603_1608Metric",
        "x": 30.00,
        "y": 1.70,
        "rot": 90.0
    }
]

# Remove existing if any
for c in caps:
    for r in c["alt_refs"]:
        fp = board.FindFootprintByReference(r)
        if fp:
            print(f"Removing existing footprint {r}")
            board.Remove(fp)

# Place new footprints
for c in caps:
    fp = pcbnew.FootprintLoad(c["fp_lib"], c["fp_name"])
    if not fp:
        raise RuntimeError(f"Failed to load {c['fp_name']} from {c['fp_lib']}")
    board.Add(fp)
    fp.SetReference(c["ref"])
    fp.SetValue(c["val"])
    fp.SetPosition(pcbnew.VECTOR2I(pcbnew.FromMM(c["x"]), pcbnew.FromMM(c["y"])))
    fp.SetOrientation(pcbnew.EDA_ANGLE(c["rot"], pcbnew.DEGREES_T))
    fp.Reference().SetVisible(False)
    fp.Value().SetVisible(False)
    print(f"Placed {c['ref']} ({c['val']}) at ({c['x']}, {c['y']}) rot={c['rot']}°")

pcbnew.SaveBoard(pcb_path, board)
print("Saved updated PCB.")

# 3. Update Schematic with C_SSR1 and C_SSR2
with open(sch_path, "r", encoding="utf-8") as f:
    sch_text = f.read()

# Check if C_SSR1 or C_SSR2 already in schematic
if "C_SSR1" not in sch_text:
    sch_c_additions = f'''
	(symbol (lib_id "Device:C")
		(at 165.0 25.0 0)
		(unit 1)
		(exclude_from_sim no)
		(in_bom yes)
		(on_board yes)
		(dnp no)
		(uuid "{uuid.uuid4()}")
		(property "Reference" "C_SSR1" (at 165.0 21.0 0) (effects (font (size 1.27 1.27))))
		(property "Value" "100nF" (at 165.0 29.0 0) (effects (font (size 1.27 1.27))))
		(property "Footprint" "Capacitor_SMD:C_0603_1608Metric" (at 165.0 25.0 0) (hide yes) (effects (font (size 1.27 1.27))))
		(pin "1" (uuid "{uuid.uuid4()}"))
		(pin "2" (uuid "{uuid.uuid4()}"))
		(instances
			(project "qfbms32"
				(path "/a2322edc-ff52-449c-92df-24faffac0236" (reference "C_SSR1") (unit 1))
			)
		)
	)

	(symbol (lib_id "Device:C")
		(at 175.0 25.0 0)
		(unit 1)
		(exclude_from_sim no)
		(in_bom yes)
		(on_board yes)
		(dnp no)
		(uuid "{uuid.uuid4()}")
		(property "Reference" "C_SSR2" (at 175.0 21.0 0) (effects (font (size 1.27 1.27))))
		(property "Value" "1uF" (at 175.0 29.0 0) (effects (font (size 1.27 1.27))))
		(property "Footprint" "Capacitor_SMD:C_0603_1608Metric" (at 175.0 25.0 0) (hide yes) (effects (font (size 1.27 1.27))))
		(pin "1" (uuid "{uuid.uuid4()}"))
		(pin "2" (uuid "{uuid.uuid4()}"))
		(instances
			(project "qfbms32"
				(path "/a2322edc-ff52-449c-92df-24faffac0236" (reference "C_SSR2") (unit 1))
			)
		)
	)
'''
    insert_pos = sch_text.rfind("(sheet_instances")
    if insert_pos != -1:
        sch_text = sch_text[:insert_pos] + sch_c_additions + "\n\t" + sch_text[insert_pos:]
        with open(sch_path, "w", encoding="utf-8") as f:
            f.write(sch_text)
        print("Updated schematic with C_SSR1 and C_SSR2.")

# 4. Update qfbms32.boxes.json
with open(boxes_path, "r", encoding="utf-8") as f:
    boxes_data = json.load(f)

for col in boxes_data.get("colors", []):
    if col["id"] == "cybmnt2eg7":
        col["note"] = "C_SSR1 (0603 100nF light tan cap)"
    elif col["id"] == "csmn6nzgf0":
        col["note"] = "C_SSR2 (0603 1uF darker orange cap)"

for b in boxes_data.get("boxes", []):
    if b["id"] == "bju2jyl3bq":
        b["ref"] = "C_SSR1"
        b["val"] = "100nF"
        b["fpid"] = "Capacitor_SMD:C_0603_1608Metric"
    elif b["id"] == "b8pftw96rl":
        b["ref"] = "C_SSR2"
        b["val"] = "1uF"
        b["fpid"] = "Capacitor_SMD:C_0603_1608Metric"

with open(boxes_path, "w", encoding="utf-8") as f:
    json.dump(boxes_data, f, indent=1)
print("Updated qfbms32.boxes.json.")

# 5. Render top 3D and iso 3D
raw_top_png = os.path.join(pcb_dir, "qfbms32_layout_top_hi_raw.png")
top_3d_png = os.path.join(pcb_dir, "qfbms32_3d_top.png")
iso_3d_png = os.path.join(pcb_dir, "qfbms32_3d_iso.png")

print("Rendering top 3D view...")
subprocess.run([
    kicad_cli, "pcb", "render",
    "--side", "top",
    "--width", "4000", "--height", "2000",
    "--background", "transparent",
    "-o", raw_top_png, pcb_path
], capture_output=True, text=True)

if os.path.exists(raw_top_png):
    im = Image.open(raw_top_png)
    bbox = im.getbbox()
    if bbox:
        pad = 30
        crop_box = (max(0, bbox[0]-pad), max(0, bbox[1]-pad), min(im.width, bbox[2]+pad), min(im.height, bbox[3]+pad))
        im.crop(crop_box).save(top_3d_png)
        print(f"Saved {top_3d_png}")

print("Rendering isometric 3D view...")
subprocess.run([
    kicad_cli, "pcb", "render",
    "--rotate", "-45,0,45",
    "--width", "4000", "--height", "2600",
    "--background", "transparent",
    "-o", iso_3d_png, pcb_path
], capture_output=True, text=True)

if os.path.exists(iso_3d_png):
    im = Image.open(iso_3d_png)
    bbox = im.getbbox()
    if bbox:
        pad = 20
        crop_box = (max(0, bbox[0]-pad), max(0, bbox[1]-pad), min(im.width, bbox[2]+pad), min(im.height, bbox[3]+pad))
        im.crop(crop_box).save(iso_3d_png)
        print(f"Saved {iso_3d_png}")

# 6. Generate Annotated Preview
import sys
sys.path.insert(0, pcb_dir)
import generate_annotated_preview
generate_annotated_preview.generate_annotated_preview()
print("Generated annotated preview.")

# 7. Copy artifacts to brain directory
shutil.copy2(top_3d_png, os.path.join(brain_dir, "qfbms32_3d_top.png"))
shutil.copy2(iso_3d_png, os.path.join(brain_dir, "qfbms32_3d_iso.png"))
labeled_png = os.path.join(pcb_dir, "qfbms32_layout_labeled.png")
if os.path.exists(labeled_png):
    shutil.copy2(labeled_png, os.path.join(brain_dir, "qfbms32_layout_labeled.png"))

print("All tasks finished successfully!")
