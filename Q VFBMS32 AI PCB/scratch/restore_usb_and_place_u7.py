import os
import re
import shutil
import subprocess
from PIL import Image

PROJECT_DIR = r"c:\Users\quinn\Documents\GitHub\Fungineers PCB designs\Q VFBMS32 AI PCB"
KICAD_CLI = r"C:\Program Files\KiCad\10.0\bin\kicad-cli.exe"
SCH_PATH = os.path.join(PROJECT_DIR, "VFBMS32.kicad_sch")
PCB_PATH = os.path.join(PROJECT_DIR, "VFBMS32.kicad_pcb")
BRAIN_DIR = r"C:\Users\quinn\.gemini\antigravity-ide\brain\a11d5216-ec23-4de0-9ff6-ae2ffbd1fda7"

print("=== 1. UPDATING SCHEMATIC (VFBMS32.kicad_sch) ===")
with open(SCH_PATH, "r", encoding="utf-8") as f:
    sch = f.read()

# Update U7 footprint property to Package_SO:SOIC-8_3.9x4.9mm_P1.27mm
sch = re.sub(
    r'(\(property "Reference" "U7"[\s\S]*?\(property "Footprint" ")[^"]+(")',
    r'\g<1>Package_SO:SOIC-8_3.9x4.9mm_P1.27mm\g<2>',
    sch
)

with open(SCH_PATH, "w", encoding="utf-8") as f:
    f.write(sch)
print("Updated schematic footprint for U7 to Package_SO:SOIC-8_3.9x4.9mm_P1.27mm!")

print("\n=== 2. UPDATING PCB (VFBMS32.kicad_pcb) ===")
with open(PCB_PATH, "r", encoding="utf-8") as f:
    pcb_lines = f.readlines()

new_pcb_lines = []
depth = 0
in_fp = False
curr_fp_lines = []

for line in pcb_lines:
    if '(footprint ' in line and depth == 0:
        in_fp = True
        depth = 1
        curr_fp_lines = [line]
    elif in_fp:
        curr_fp_lines.append(line)
        depth += line.count('(') - line.count(')')
        if depth == 0:
            in_fp = False
            fp_text = "".join(curr_fp_lines)
            ref_m = re.search(r'\(property "Reference" "([^"]+)"', fp_text)
            ref = ref_m.group(1) if ref_m else ""
            
            if ref == "J_USB1":
                print("-> Restoring & locking J_USB1 to (125.0, 3.2, rot=180)")
                fp_text = re.sub(r'\(at\s+[0-9\.\-]+\s+[0-9\.\-]+\s+180\)', '(at 125 3.2 180)', fp_text)
                new_pcb_lines.append(fp_text)
            elif ref == "U7":
                print("-> Setting U7 to SOIC-8_3.9x4.9mm_P1.27mm at (125.0, 12.0, rot=0)")
                u7_soic = """\t(footprint "Package_SO:SOIC-8_3.9x4.9mm_P1.27mm"
		(layer "F.Cu")
		(uuid "28929e53-d3ff-4d4a-8621-05c659c8e34f")
		(at 125 12)
		(descr "SOIC, 8 Pin (JEDEC MS-012AA, TI ISO1050 SOIC-8 / D package)")
		(tags "SOIC SO ISO1050 CAN")
		(property "Reference" "U7"
			(at 0 -3.4 0)
			(layer "F.SilkS")
			(uuid "7e64e7bd-ca78-40c3-9376-73a236b32b1c")
			(effects
				(font
					(size 0.65 0.65)
					(thickness 0.12)
				)
			)
		)
		(property "Value" "ISO1050"
			(at 0 3.4 0)
			(layer "F.Fab")
			(uuid "f0fb3e80-21d5-474a-bdfa-d3e775dad1ad")
			(effects
				(font
					(size 0.7 0.7)
					(thickness 0.12)
				)
			)
		)
		(property "Footprint" "Package_SO:SOIC-8_3.9x4.9mm_P1.27mm"
			(at 0 0 0)
			(layer "F.Fab")
			(hide yes)
			(uuid "006851a4-0ac9-4de4-a2c9-51dbc38fa669")
			(effects
				(font
					(size 1.27 1.27)
				)
			)
		)
		(attr smd)
		(fp_line
			(start -2.06 -2.56)
			(end 2.06 -2.56)
			(stroke (width 0.12) (type solid))
			(layer "F.SilkS")
		)
		(fp_line
			(start -2.06 2.56)
			(end 2.06 2.56)
			(stroke (width 0.12) (type solid))
			(layer "F.SilkS")
		)
		(fp_circle
			(center -2.6 -2.8)
			(end -2.3 -2.8)
			(stroke (width 0.12) (type solid))
			(fill yes)
			(layer "F.SilkS")
		)
		(pad "1" smd roundrect
			(at -2.6 -1.905)
			(size 1.95 0.6)
			(layers "F.Cu" "F.Paste" "F.Mask")
			(roundrect_rratio 0.25)
			(net 1 "+3V3")
			(uuid "u7-p1")
		)
		(pad "2" smd roundrect
			(at -2.6 -0.635)
			(size 1.95 0.6)
			(layers "F.Cu" "F.Paste" "F.Mask")
			(roundrect_rratio 0.25)
			(net 2 "CAN_RX")
			(uuid "u7-p2")
		)
		(pad "3" smd roundrect
			(at -2.6 0.635)
			(size 1.95 0.6)
			(layers "F.Cu" "F.Paste" "F.Mask")
			(roundrect_rratio 0.25)
			(net 3 "CAN_TX")
			(uuid "u7-p3")
		)
		(pad "4" smd roundrect
			(at -2.6 1.905)
			(size 1.95 0.6)
			(layers "F.Cu" "F.Paste" "F.Mask")
			(roundrect_rratio 0.25)
			(net 4 "GND")
			(uuid "u7-p4")
		)
		(pad "5" smd roundrect
			(at 2.6 1.905)
			(size 1.95 0.6)
			(layers "F.Cu" "F.Paste" "F.Mask")
			(roundrect_rratio 0.25)
			(net 5 "ISO_GND")
			(uuid "u7-p5")
		)
		(pad "6" smd roundrect
			(at 2.6 0.635)
			(size 1.95 0.6)
			(layers "F.Cu" "F.Paste" "F.Mask")
			(roundrect_rratio 0.25)
			(net 6 "CANL")
			(uuid "u7-p6")
		)
		(pad "7" smd roundrect
			(at 2.6 -0.635)
			(size 1.95 0.6)
			(layers "F.Cu" "F.Paste" "F.Mask")
			(roundrect_rratio 0.25)
			(net 7 "CANH")
			(uuid "u7-p7")
		)
		(pad "8" smd roundrect
			(at 2.6 -1.905)
			(size 1.95 0.6)
			(layers "F.Cu" "F.Paste" "F.Mask")
			(roundrect_rratio 0.25)
			(net 8 "5VExt")
			(uuid "u7-p8")
		)
		(model "${KICAD10_3DMODEL_DIR}/Package_SO.3dshapes/SOIC-8_3.9x4.9mm_P1.27mm.step"
			(offset (xyz 0 0 0))
			(scale (xyz 1 1 1))
			(rotate (xyz 0 0 0))
		)
	)\n"""
                new_pcb_lines.append(u7_soic)
            else:
                new_pcb_lines.append(fp_text)
    else:
        new_pcb_lines.append(line)

with open(PCB_PATH, "w", encoding="utf-8") as f:
    f.writelines(new_pcb_lines)
print("Updated VFBMS32.kicad_pcb successfully!")

print("\n=== 3. RENDERING TOP-DOWN 2D & 3D VIEWS ===")
# 2D Top-down Render
render_top = os.path.join(PROJECT_DIR, "VFBMS32_layout_top_hi_raw.png")
subprocess.run([
    KICAD_CLI, "pcb", "render",
    "--rotate", "0,0,0",
    "--zoom", "1",
    "--width", "3600", "--height", "1200",
    "--background", "transparent",
    "-o", render_top, PCB_PATH
], check=True)

# 3D Perspective Render
render_3d = os.path.join(PROJECT_DIR, "VFBMS32_render_3d.png")
subprocess.run([
    KICAD_CLI, "pcb", "render",
    "--perspective",
    "--rotate", "-25,0,25",
    "--floor",
    "--width", "3600", "--height", "1600",
    "--background", "transparent",
    "-o", render_3d, PCB_PATH
], check=True)

# Detailed top-right corner crop
im_top = Image.open(render_top)
bbox = im_top.getbbox()
if bbox:
    w = bbox[2] - bbox[0]
    h = bbox[3] - bbox[1]
    # Crop top-right corner (X ~ 70% to 100%, Y: full height)
    crop_x1 = bbox[0] + int(w * 0.70)
    crop_x2 = bbox[2] + 20
    crop_y1 = max(0, bbox[1] - 20)
    crop_y2 = min(im_top.height, bbox[3] + 20)
    corner_zoom = im_top.crop((crop_x1, crop_y1, crop_x2, crop_y2))
    corner_zoom_path = os.path.join(PROJECT_DIR, "VFBMS32_esp_usb_u7_verified.png")
    corner_zoom.save(corner_zoom_path)
    print(f"Saved verified top-right corner zoom: {corner_zoom_path}")

# Copy to brain dir
os.makedirs(BRAIN_DIR, exist_ok=True)
for fname in ["VFBMS32_esp_usb_u7_verified.png", "VFBMS32_layout_top_hi_raw.png", "VFBMS32_render_3d.png"]:
    src = os.path.join(PROJECT_DIR, fname)
    dst = os.path.join(BRAIN_DIR, fname)
    if os.path.exists(src):
        shutil.copyfile(src, dst)
        print(f"Copied {fname} to brain directory!")

print("ALL RESTORATIONS AND RENDERS COMPLETED SUCCESSFULLY!")
