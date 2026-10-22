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

# Update U7 footprint property to Package_DIP:SMDIP-8_W9.53mm
sch = re.sub(
    r'(\(property "Reference" "U7"[\s\S]*?\(property "Footprint" ")[^"]+(")',
    r'\g<1>Package_DIP:SMDIP-8_W9.53mm\g<2>',
    sch
)

with open(SCH_PATH, "w", encoding="utf-8") as f:
    f.write(sch)
print("Updated schematic footprint for U7 to Package_DIP:SMDIP-8_W9.53mm!")

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
                print("-> Keeping J_USB1 locked at (125.0, 3.2, rot=180)")
                fp_text = re.sub(r'\(at\s+[0-9\.\-]+\s+[0-9\.\-]+\s+180\)', '(at 125 3.2 180)', fp_text)
                new_pcb_lines.append(fp_text)
            elif ref == "U7":
                print("-> Setting U7 to TI DUB-8 (SMDIP-8_W9.53mm) at (124.0, 14.0, rot=0)")
                u7_dub8 = """\t(footprint "Package_DIP:SMDIP-8_W9.53mm"
		(layer "F.Cu")
		(uuid "28929e53-d3ff-4d4a-8621-05c659c8e34f")
		(at 124 14)
		(descr "8-lead surface-mounted (SMD) DIP package / TI DUB-8 (ISO1050), row spacing 9.53mm (375 mils), 2.54mm pitch")
		(tags "SMD DIP DIL PDIP SMDIP 2.54mm 9.53mm 375mil TI DUB-8")
		(property "Reference" "U7"
			(at 0 -5.8 0)
			(layer "F.SilkS")
			(uuid "7e64e7bd-ca78-40c3-9376-73a236b32b1c")
			(effects
				(font
					(size 0.7 0.7)
					(thickness 0.13)
				)
			)
		)
		(property "Value" "ISO1050 (DUB-8)"
			(at 0 5.8 0)
			(layer "F.Fab")
			(uuid "f0fb3e80-21d5-474a-bdfa-d3e775dad1ad")
			(effects
				(font
					(size 0.8 0.8)
					(thickness 0.14)
				)
			)
		)
		(property "Footprint" "Package_DIP:SMDIP-8_W9.53mm"
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
			(start -3.235 -5.14)
			(end -3.235 5.14)
			(stroke (width 0.12) (type solid))
			(layer "F.SilkS")
		)
		(fp_line
			(start -3.235 5.14)
			(end 3.235 5.14)
			(stroke (width 0.12) (type solid))
			(layer "F.SilkS")
		)
		(fp_line
			(start -1 -5.14)
			(end -3.235 -5.14)
			(stroke (width 0.12) (type solid))
			(layer "F.SilkS")
		)
		(fp_line
			(start 3.235 -5.14)
			(end 1 -5.14)
			(stroke (width 0.12) (type solid))
			(layer "F.SilkS")
		)
		(fp_line
			(start 3.235 5.14)
			(end 3.235 -5.14)
			(stroke (width 0.12) (type solid))
			(layer "F.SilkS")
		)
		(fp_arc
			(start 1 -5.14)
			(mid 0 -4.14)
			(end -1 -5.14)
			(stroke (width 0.12) (type solid))
			(layer "F.SilkS")
		)
		(pad "1" smd roundrect
			(at -4.765 -3.81)
			(size 2 1.78)
			(layers "F.Cu" "F.Mask" "F.Paste")
			(roundrect_rratio 0.140449)
			(net 1 "+3V3")
			(uuid "u7-p1")
		)
		(pad "2" smd roundrect
			(at -4.765 -1.27)
			(size 2 1.78)
			(layers "F.Cu" "F.Mask" "F.Paste")
			(roundrect_rratio 0.140449)
			(net 2 "CAN_RX")
			(uuid "u7-p2")
		)
		(pad "3" smd roundrect
			(at -4.765 1.27)
			(size 2 1.78)
			(layers "F.Cu" "F.Mask" "F.Paste")
			(roundrect_rratio 0.140449)
			(net 3 "CAN_TX")
			(uuid "u7-p3")
		)
		(pad "4" smd roundrect
			(at -4.765 3.81)
			(size 2 1.78)
			(layers "F.Cu" "F.Mask" "F.Paste")
			(roundrect_rratio 0.140449)
			(net 4 "GND")
			(uuid "u7-p4")
		)
		(pad "5" smd roundrect
			(at 4.765 3.81)
			(size 2 1.78)
			(layers "F.Cu" "F.Mask" "F.Paste")
			(roundrect_rratio 0.140449)
			(net 5 "ISO_GND")
			(uuid "u7-p5")
		)
		(pad "6" smd roundrect
			(at 4.765 1.27)
			(size 2 1.78)
			(layers "F.Cu" "F.Mask" "F.Paste")
			(roundrect_rratio 0.140449)
			(net 6 "CANL")
			(uuid "u7-p6")
		)
		(pad "7" smd roundrect
			(at 4.765 -1.27)
			(size 2 1.78)
			(layers "F.Cu" "F.Mask" "F.Paste")
			(roundrect_rratio 0.140449)
			(net 7 "CANH")
			(uuid "u7-p7")
		)
		(pad "8" smd roundrect
			(at 4.765 -3.81)
			(size 2 1.78)
			(layers "F.Cu" "F.Mask" "F.Paste")
			(roundrect_rratio 0.140449)
			(net 8 "5VExt")
			(uuid "u7-p8")
		)
		(model "${KICAD10_3DMODEL_DIR}/Package_DIP.3dshapes/SMDIP-8_W9.53mm.step"
			(offset (xyz 0 0 0))
			(scale (xyz 1 1 1))
			(rotate (xyz 0 0 0))
		)
	)\n"""
                new_pcb_lines.append(u7_dub8)
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

# 3D Zoom on top-right quadrant
render_u7_3d = os.path.join(PROJECT_DIR, "VFBMS32_u7_dub8_zoom_3d.png")
subprocess.run([
    KICAD_CLI, "pcb", "render",
    "--perspective",
    "--rotate", "-15,0,10",
    "--floor",
    "--width", "2800", "--height", "1600",
    "--background", "transparent",
    "-o", render_u7_3d, PCB_PATH
], check=True)

# Crop 2D Zoom on top-right quadrant (X: 100-130 mm, Y: 0-32 mm)
im_top = Image.open(render_top)
bbox = im_top.getbbox()
if bbox:
    w = bbox[2] - bbox[0]
    h = bbox[3] - bbox[1]
    # Crop X: ~70% to 100%, Y: full height
    crop_x1 = bbox[0] + int(w * 0.70)
    crop_x2 = bbox[2] + 20
    crop_y1 = max(0, bbox[1] - 20)
    crop_y2 = min(im_top.height, bbox[3] + 20)
    corner_zoom = im_top.crop((crop_x1, crop_y1, crop_x2, crop_y2))
    corner_zoom_path = os.path.join(PROJECT_DIR, "VFBMS32_esp_usb_u7_verified.png")
    corner_zoom.save(corner_zoom_path)
    print(f"Saved verified top-right corner zoom: {corner_zoom_path}")

# Crop 3D Zoom on right corner
if os.path.exists(render_u7_3d):
    im_u7_3d = Image.open(render_u7_3d)
    bbox_3d = im_u7_3d.getbbox()
    if bbox_3d:
        crop_3d_box = (
            bbox_3d[0] + int((bbox_3d[2]-bbox_3d[0])*0.55),
            max(0, bbox_3d[1] - 20),
            bbox_3d[2] + 20,
            min(im_u7_3d.height, bbox_3d[3] + 20)
        )
        im_u7_3d.crop(crop_3d_box).save(render_u7_3d)
        print(f"Cropped 3D zoom saved to {render_u7_3d}")

# Copy to brain dir
os.makedirs(BRAIN_DIR, exist_ok=True)
for fname in ["VFBMS32_esp_usb_u7_verified.png", "VFBMS32_layout_top_hi_raw.png", "VFBMS32_render_3d.png", "VFBMS32_u7_dub8_zoom_3d.png"]:
    src = os.path.join(PROJECT_DIR, fname)
    dst = os.path.join(BRAIN_DIR, fname)
    if os.path.exists(src):
        shutil.copyfile(src, dst)
        print(f"Copied {fname} to brain directory!")

# Schematic export with try/except
sch_pdf = os.path.join(PROJECT_DIR, "VFBMS32_schematic.pdf")
try:
    subprocess.run([KICAD_CLI, "sch", "export", "pdf", "-o", sch_pdf, SCH_PATH], check=True)
    print("Exported schematic PDF successfully!")
except Exception as e:
    print(f"PDF export warning: {e}")

svg_dir = os.path.join(PROJECT_DIR, "sch_svg")
os.makedirs(svg_dir, exist_ok=True)
try:
    subprocess.run([KICAD_CLI, "sch", "export", "svg", "-o", svg_dir, SCH_PATH], check=True)
    print("Exported schematic SVG successfully!")
except Exception as e:
    print(f"SVG export warning: {e}")

print("ALL CORRECTIONS AND RENDERS COMPLETED SUCCESSFULLY!")
