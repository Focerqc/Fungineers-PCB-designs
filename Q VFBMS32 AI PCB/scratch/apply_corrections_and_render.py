import os
import re
import shutil
import subprocess
from PIL import Image

PROJECT_DIR = r"c:\Users\quinn\Documents\GitHub\Fungineers PCB designs\Q VFBMS32 AI PCB"
KICAD_CLI = r"C:\Program Files\KiCad\10.0\bin\kicad-cli.exe"
SCH_PATH = os.path.join(PROJECT_DIR, "VFBMS32.kicad_sch")
PCB_PATH = os.path.join(PROJECT_DIR, "VFBMS32.kicad_pcb")

print("=== 1. UPDATING SCHEMATIC (VFBMS32.kicad_sch) ===")
with open(SCH_PATH, "r", encoding="utf-8") as f:
    sch_content = f.read()

# 1a. Remove any L2 symbol if present
sch_content = re.sub(r'\(symbol\s+\(lib_id\s+"[^"]*"\)[\s\S]*?\(property\s+"Reference"\s+"L2"[\s\S]*?\n\t\)', '', sch_content)

# 1b. Replace SN65HVD230 / CH340 / U5 with U7 (ISO1050DUB)
# Let's ensure ISO1050DUB is in lib_symbols
iso_lib_symbol = """		(symbol "Interface_CAN_LIN:ISO1050DUB"
			(exclude_from_sim no)
			(in_bom yes)
			(on_board yes)
			(in_pos_files yes)
			(duplicate_pin_numbers_are_jumpers no)
			(property "Reference" "U"
				(at -6.35 6.35 0)
				(show_name no)
				(do_not_autoplace no)
				(effects
					(font
						(size 1.27 1.27)
					)
				)
			)
			(property "Value" "ISO1050DUB"
				(at 2.54 6.35 0)
				(show_name no)
				(do_not_autoplace no)
				(effects
					(font
						(size 1.27 1.27)
					)
				)
			)
			(property "Footprint" "Package_SO:SOIC-8_7.5x5.85mm_P1.27mm"
				(at 0 -8.89 0)
				(show_name no)
				(do_not_autoplace no)
				(hide yes)
				(effects
					(font
						(size 1.27 1.27)
						(italic yes)
					)
				)
			)
			(property "Datasheet" "http://www.ti.com/lit/ds/symlink/iso1050.pdf"
				(at 0 -1.27 0)
				(show_name no)
				(do_not_autoplace no)
				(hide yes)
				(effects
					(font
						(size 1.27 1.27)
					)
				)
			)
			(property "Description" "Isolated CAN Transceiver, SOIC-8 Wide"
				(at 0 0 0)
				(show_name no)
				(do_not_autoplace no)
				(hide yes)
				(effects
					(font
						(size 1.27 1.27)
					)
				)
			)
			(property "ki_keywords" "CAN Isolated Transceiver"
				(at 0 0 0)
				(show_name no)
				(do_not_autoplace no)
				(hide yes)
				(effects
					(font
						(size 1.27 1.27)
					)
				)
			)
			(symbol "ISO1050DUB_0_1"
				(rectangle
					(start -7.62 5.08)
					(end 7.62 -7.62)
					(stroke
						(width 0.254)
						(type default)
					)
					(fill
						(type background)
					)
				)
				(polyline
					(pts
						(xy 0 5.08) (xy 0 -7.62)
					)
					(stroke
						(width 0.2)
						(type dash)
					)
					(fill
						(type none)
					)
				)
			)
			(symbol "ISO1050DUB_1_1"
				(pin power_in line
					(at -10.16 2.54 0)
					(length 2.54)
					(name "VCC1"
						(effects
							(font
								(size 1.27 1.27)
							)
						)
					)
					(number "1"
						(effects
							(font
								(size 1.27 1.27)
							)
						)
					)
				)
				(pin output line
					(at -10.16 0 0)
					(length 2.54)
					(name "RXD"
						(effects
							(font
								(size 1.27 1.27)
							)
						)
					)
					(number "2"
						(effects
							(font
								(size 1.27 1.27)
							)
						)
					)
				)
				(pin input line
					(at -10.16 -2.54 0)
					(length 2.54)
					(name "TXD"
						(effects
							(font
								(size 1.27 1.27)
							)
						)
					)
					(number "3"
						(effects
							(font
								(size 1.27 1.27)
							)
						)
					)
				)
				(pin power_in line
					(at -10.16 -5.08 0)
					(length 2.54)
					(name "GND1"
						(effects
							(font
								(size 1.27 1.27)
							)
						)
					)
					(number "4"
						(effects
							(font
								(size 1.27 1.27)
							)
						)
					)
				)
				(pin power_in line
					(at 10.16 -5.08 180)
					(length 2.54)
					(name "GND2"
						(effects
							(font
								(size 1.27 1.27)
							)
						)
					)
					(number "5"
						(effects
							(font
								(size 1.27 1.27)
							)
						)
					)
				)
				(pin bidirectional line
					(at 10.16 -2.54 180)
					(length 2.54)
					(name "CANL"
						(effects
							(font
								(size 1.27 1.27)
							)
						)
					)
					(number "6"
						(effects
							(font
								(size 1.27 1.27)
							)
						)
					)
				)
				(pin bidirectional line
					(at 10.16 0 180)
					(length 2.54)
					(name "CANH"
						(effects
							(font
								(size 1.27 1.27)
							)
						)
					)
					(number "7"
						(effects
							(font
								(size 1.27 1.27)
							)
						)
					)
				)
				(pin power_in line
					(at 10.16 2.54 180)
					(length 2.54)
					(name "VCC2"
						(effects
							(font
								(size 1.27 1.27)
							)
						)
					)
					(number "8"
						(effects
							(font
								(size 1.27 1.27)
							)
						)
					)
				)
			)
		)"""

if "symbol \"Interface_CAN_LIN:ISO1050DUB\"" not in sch_content:
    # Insert before the end of lib_symbols
    sch_content = sch_content.replace('\t(lib_symbols', f'\t(lib_symbols\n{iso_lib_symbol}')

# Remove old U5 / SN65HVD230 symbol instance
sch_content = re.sub(r'\(symbol\s+\(lib_id\s+"Interface_CAN_LIN:SN65HVD230"\)[\s\S]*?\n\t\)', '', sch_content)

# Add U7 (ISO1050) symbol instance
u7_instance = """\t(symbol
		(lib_id "Interface_CAN_LIN:ISO1050DUB")
		(at 59.69 229.87 0)
		(unit 1)
		(body_style 1)
		(exclude_from_sim no)
		(in_bom yes)
		(on_board yes)
		(in_pos_files yes)
		(dnp no)
		(uuid "62122533-64a6-46b3-9e24-7da6511c76f2")
		(property "Reference" "U7"
			(at 57.15 240.03 0)
			(show_name no)
			(do_not_autoplace no)
			(effects
				(font
					(size 1.27 1.27)
				)
				(justify right)
			)
		)
		(property "Value" "ISO1050 (Isolated CAN Transceiver)"
			(at 57.15 237.49 0)
			(show_name no)
			(do_not_autoplace no)
			(effects
				(font
					(size 1.27 1.27)
				)
				(justify right)
			)
		)
		(property "Footprint" "Package_SO:SOIC-8_7.5x5.85mm_P1.27mm"
			(at 59.69 217.17 0)
			(hide yes)
			(show_name no)
			(do_not_autoplace no)
			(effects
				(font
					(size 1.27 1.27)
				)
			)
		)
		(property "Datasheet" "http://www.ti.com/lit/ds/symlink/iso1050.pdf"
			(at 57.15 240.03 0)
			(hide yes)
			(show_name no)
			(do_not_autoplace no)
			(effects
				(font
					(size 1.27 1.27)
				)
			)
		)
		(property "Description" "Isolated 5V CAN Transceiver, SOIC-8 Wide"
			(at 59.69 229.87 0)
			(hide yes)
			(show_name no)
			(do_not_autoplace no)
			(effects
				(font
					(size 1.27 1.27)
				)
			)
		)
		(pin "1" (uuid "u7-pin-1"))
		(pin "2" (uuid "u7-pin-2"))
		(pin "3" (uuid "u7-pin-3"))
		(pin "4" (uuid "u7-pin-4"))
		(pin "5" (uuid "u7-pin-5"))
		(pin "6" (uuid "u7-pin-6"))
		(pin "7" (uuid "u7-pin-7"))
		(pin "8" (uuid "u7-pin-8"))
		(instances
			(project "VFBMS32"
				(path "/a2322edc-ff52-449c-92df-24faffac0236"
					(reference "U7")
					(unit 1)
				)
			)
		)
	)"""

# Append U7 instance if not present
if '(property "Reference" "U7"' not in sch_content:
    # Insert before final closing parenthesis
    last_paren = sch_content.rfind(')')
    sch_content = sch_content[:last_paren] + u7_instance + "\n)\n"

# Ensure USB labels exist for ESP32 and USB connector
labels_to_add = [
    '(label "USB_D-" (at 36.83 107.95 180) (fields_autoplaced yes) (effects (font (size 1.27 1.27)) (justify right)) (uuid "usb-dm-label"))',
    '(label "USB_D+" (at 36.83 105.41 180) (fields_autoplaced yes) (effects (font (size 1.27 1.27)) (justify right)) (uuid "usb-dp-label"))',
    '(label "5VExt" (at 69.85 232.41 0) (fields_autoplaced yes) (effects (font (size 1.27 1.27)) (justify left)) (uuid "5vext-label"))',
    '(label "ISO_GND" (at 69.85 224.79 0) (fields_autoplaced yes) (effects (font (size 1.27 1.27)) (justify left)) (uuid "isognd-label"))',
    '(label "CANH" (at 69.85 229.87 0) (fields_autoplaced yes) (effects (font (size 1.27 1.27)) (justify left)) (uuid "canh-label"))',
    '(label "CANL" (at 69.85 227.33 0) (fields_autoplaced yes) (effects (font (size 1.27 1.27)) (justify left)) (uuid "canl-label"))',
    '(label "+3V3" (at 49.53 232.41 180) (fields_autoplaced yes) (effects (font (size 1.27 1.27)) (justify right)) (uuid "vcc1-label"))',
    '(label "GND" (at 49.53 224.79 180) (fields_autoplaced yes) (effects (font (size 1.27 1.27)) (justify right)) (uuid "gnd1-label"))',
]

for lab in labels_to_add:
    lab_name = re.search(r'label "([^"]+)"', lab).group(1)
    if f'label "{lab_name}"' not in sch_content:
        last_paren = sch_content.rfind(')')
        sch_content = sch_content[:last_paren] + "\t" + lab + "\n)\n"

with open(SCH_PATH, "w", encoding="utf-8") as f:
    f.write(sch_content)
print("Updated VFBMS32.kicad_sch successfully!")

print("\n=== 2. UPDATING PCB (VFBMS32.kicad_pcb) ===")
with open(PCB_PATH, "r", encoding="utf-8") as f:
    pcb_lines = f.readlines()

# Parse footprints out
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
            
            if ref == "L2":
                print("-> Removed Ghost Inductor L2 from PCB!")
                continue
            elif ref == "L1":
                # Fix L1 3D model path to valid KiCad 10 step model
                print("-> Updating L1 3D model to L_SXN_SMDRI73.step")
                # Replace model block
                fp_text = re.sub(r'\(model\s+"[^"]*"[\s\S]*?\n\t\t\)', 
                    """(model "${KICAD10_3DMODEL_DIR}/Inductor_SMD.3dshapes/L_SXN_SMDRI73.step"
			(offset
				(xyz 0 0 0)
			)
			(scale
				(xyz 1 1 1)
			)
			(rotate
				(xyz 0 0 0)
			)
		)""", fp_text)
                new_pcb_lines.append(fp_text)
            elif ref == "U7":
                print("-> Updating U7 to ISO1050 SOIC-8 Wide footprint & horizontal orientation")
                # Create updated U7 footprint block with proper pads and 3D model
                # U7 horizontal adjacent to J_USB1 (x=125, y=3.2) and ESP32 (x=106.5, y=8.5)
                # Let's place at x=124.0, y=11.5 with rot=90
                u7_fp = """\t(footprint "SOIC-8_7.5x5.85mm_P1.27mm"
		(layer "F.Cu")
		(uuid "28929e53-d3ff-4d4a-8621-05c659c8e34f")
		(at 124 11.5 90)
		(descr "SOIC-8 Wide (TI ISO1050 Isolated CAN Transceiver)")
		(tags "SOIC SOP Isolated CAN")
		(property "Reference" "U7"
			(at 0 -4.2 90)
			(layer "F.SilkS")
			(uuid "7e64e7bd-ca78-40c3-9376-73a236b32b1c")
			(effects
				(font
					(size 0.7 0.7)
					(thickness 0.13)
				)
			)
		)
		(property "Value" "ISO1050"
			(at 0 4.2 90)
			(layer "F.Fab")
			(uuid "f0fb3e80-21d5-474a-bdfa-d3e775dad1ad")
			(effects
				(font
					(size 0.8 0.8)
					(thickness 0.14)
				)
			)
		)
		(property "Footprint" "Package_SO:SOIC-8_7.5x5.85mm_P1.27mm"
			(at 0 0 90)
			(layer "F.Fab")
			(hide yes)
			(uuid "006851a4-0ac9-4de4-a2c9-51dbc38fa669")
			(effects
				(font
					(size 1.27 1.27)
				)
			)
		)
		(property "Datasheet" "http://www.ti.com/lit/ds/symlink/iso1050.pdf"
			(at 0 0 90)
			(layer "F.Fab")
			(hide yes)
			(uuid "303a4714-c220-40e6-90ae-a13b0da6c8b0")
			(effects
				(font
					(size 1.27 1.27)
				)
			)
		)
		(attr smd)
		(fp_rect
			(start -3.86 -3.035)
			(end 3.86 3.035)
			(stroke
				(width 0.12)
				(type solid)
			)
			(fill no)
			(layer "F.SilkS")
		)
		(pad "1" smd rect
			(at -3.65 -1.905 90)
			(size 1.95 0.6)
			(layers "F.Cu" "F.Paste" "F.Mask")
			(net 1 "+3V3")
			(uuid "u7-p1")
		)
		(pad "2" smd rect
			(at -3.65 -0.635 90)
			(size 1.95 0.6)
			(layers "F.Cu" "F.Paste" "F.Mask")
			(net 2 "CAN_RX")
			(uuid "u7-p2")
		)
		(pad "3" smd rect
			(at -3.65 0.635 90)
			(size 1.95 0.6)
			(layers "F.Cu" "F.Paste" "F.Mask")
			(net 3 "CAN_TX")
			(uuid "u7-p3")
		)
		(pad "4" smd rect
			(at -3.65 1.905 90)
			(size 1.95 0.6)
			(layers "F.Cu" "F.Paste" "F.Mask")
			(net 4 "GND")
			(uuid "u7-p4")
		)
		(pad "5" smd rect
			(at 3.65 1.905 90)
			(size 1.95 0.6)
			(layers "F.Cu" "F.Paste" "F.Mask")
			(net 5 "ISO_GND")
			(uuid "u7-p5")
		)
		(pad "6" smd rect
			(at 3.65 0.635 90)
			(size 1.95 0.6)
			(layers "F.Cu" "F.Paste" "F.Mask")
			(net 6 "CANL")
			(uuid "u7-p6")
		)
		(pad "7" smd rect
			(at 3.65 -0.635 90)
			(size 1.95 0.6)
			(layers "F.Cu" "F.Paste" "F.Mask")
			(net 7 "CANH")
			(uuid "u7-p7")
		)
		(pad "8" smd rect
			(at 3.65 -1.905 90)
			(size 1.95 0.6)
			(layers "F.Cu" "F.Paste" "F.Mask")
			(net 7 "5VExt")
			(uuid "u7-p8")
		)
		(model "${KICAD10_3DMODEL_DIR}/Package_SO.3dshapes/SOIC-8_7.5x5.85mm_P1.27mm.step"
			(offset
				(xyz 0 0 0)
			)
			(scale
				(xyz 1 1 1)
			)
			(rotate
				(xyz 0 0 0)
			)
		)
	)\n"""
                new_pcb_lines.append(u7_fp)
            else:
                new_pcb_lines.append(fp_text)
    else:
        new_pcb_lines.append(line)

with open(PCB_PATH, "w", encoding="utf-8") as f:
    f.writelines(new_pcb_lines)
print("Updated VFBMS32.kicad_pcb successfully!")

print("\n=== 3. RENDERING TOP-DOWN 2D & 3D VIEWS ===")
# 2D Top Render
render_top = os.path.join(PROJECT_DIR, "VFBMS32_layout_top_hi_raw.png")
subprocess.run([
    KICAD_CLI, "pcb", "render",
    "--rotate", "0,0,0",
    "--zoom", "1",
    "--width", "3600", "--height", "1200",
    "--background", "transparent",
    "-o", render_top, PCB_PATH
], check=True)
print(f"Generated 2D top render: {render_top}")

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
print(f"Generated 3D render: {render_3d}")

# Crop zoom on ESP32 / USB / U7 section
im_top = Image.open(render_top)
bbox = im_top.getbbox()
if bbox:
    w = bbox[2] - bbox[0]
    h = bbox[3] - bbox[1]
    # Crop the right 35% of the PCB
    crop_x1 = bbox[0] + int(w * 0.65)
    crop_x2 = bbox[2] + 20
    crop_y1 = max(0, bbox[1] - 20)
    crop_y2 = min(im_top.height, bbox[3] + 20)
    esp_zoom = im_top.crop((crop_x1, crop_y1, crop_x2, crop_y2))
    esp_zoom_path = os.path.join(PROJECT_DIR, "VFBMS32_esp_usb_u7_verified.png")
    esp_zoom.save(esp_zoom_path)
    print(f"Saved verified USB/ESP/U7 section: {esp_zoom_path}")

    # Also crop L1 power delivery section
    crop_l1_x1 = bbox[0] + int(w * 0.40)
    crop_l1_x2 = bbox[0] + int(w * 0.70)
    l1_zoom = im_top.crop((crop_l1_x1, crop_y1, crop_l1_x2, crop_y2))
    l1_zoom_path = os.path.join(PROJECT_DIR, "VFBMS32_l1_boost_verified.png")
    l1_zoom.save(l1_zoom_path)
    print(f"Saved verified L1 section: {l1_zoom_path}")

# Export schematic PDF and SVG
sch_pdf = os.path.join(PROJECT_DIR, "VFBMS32_schematic.pdf")
subprocess.run([KICAD_CLI, "sch", "export", "pdf", "-o", sch_pdf, SCH_PATH], check=True)
sch_svg = os.path.join(PROJECT_DIR, "VFBMS32_schematic.svg")
subprocess.run([KICAD_CLI, "sch", "export", "svg", "-o", sch_svg, SCH_PATH], check=True)
print("Exported updated schematic PDF & SVG!")
