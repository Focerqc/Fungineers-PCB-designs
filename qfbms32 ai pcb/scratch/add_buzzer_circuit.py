import os
import re
import shutil
import subprocess
from PIL import Image

PROJECT_DIR = r"c:\Users\quinn\Documents\GitHub\Fungineers PCB designs\Q VFBMS32 AI PCB"
KICAD_CLI = r"C:\Program Files\KiCad\10.0\bin\kicad-cli.exe"
SCH_PATH = os.path.join(PROJECT_DIR, "VFBMS32.kicad_sch")
PCB_PATH = os.path.join(PROJECT_DIR, "VFBMS32.kicad_pcb")

print("=== 1. UPDATING SCHEMATIC WITH BUZZER & DRIVE CIRCUIT ===")
with open(SCH_PATH, "r", encoding="utf-8") as f:
    sch = f.read()

# Add Buzzer symbol definition if needed
buzzer_lib_sym = """		(symbol "Device:Buzzer"
			(pin_numbers hide)
			(pin_names
				(offset 1.016) hide
			)
			(exclude_from_sim no)
			(in_bom yes)
			(on_board yes)
			(in_pos_files yes)
			(property "Reference" "BZ"
				(at 0 2.54 0)
				(effects
					(font
						(size 1.27 1.27)
					)
				)
			)
			(property "Value" "Buzzer"
				(at 0 -2.54 0)
				(effects
					(font
						(size 1.27 1.27)
					)
				)
			)
			(property "Footprint" ""
				(at 0 0 0)
				(hide yes)
				(effects
					(font
						(size 1.27 1.27)
					)
				)
			)
			(property "Description" "Buzzer, polarized"
				(at 0 0 0)
				(hide yes)
				(effects
					(font
						(size 1.27 1.27)
					)
				)
			)
			(symbol "Buzzer_0_1"
				(polyline
					(pts
						(xy -2.54 1.27) (xy -2.54 -1.27) (xy 2.54 -1.27) (xy 2.54 1.27) (xy -2.54 1.27)
					)
					(stroke
						(width 0.254)
						(type default)
					)
					(fill
						(type background)
					)
				)
			)
			(symbol "Buzzer_1_1"
				(pin passive line
					(at -5.08 0 0)
					(length 2.54)
					(name "+"
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
				(pin passive line
					(at 5.08 0 180)
					(length 2.54)
					(name "-"
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
			)
		)"""

if 'symbol "Device:Buzzer"' not in sch:
    sch = sch.replace('\t(lib_symbols', f'\t(lib_symbols\n{buzzer_lib_sym}')

# Buzzer circuit instances
buzzer_instances = """\t(symbol
		(lib_id "Device:Buzzer")
		(at 85.0 230.0 0)
		(unit 1)
		(property "Reference" "BZ1"
			(at 85.0 226.0 0)
			(effects (font (size 1.27 1.27)))
		)
		(property "Value" "MLT-5030 (3.3V Buzzer)"
			(at 85.0 234.0 0)
			(effects (font (size 1.27 1.27)))
		)
		(property "Footprint" "vfbms:Buzzer_5.0x5.0mm_SMD"
			(at 85.0 230.0 0)
			(hide yes)
			(effects (font (size 1.27 1.27)))
		)
		(pin "1" (uuid "bz1-p1"))
		(pin "2" (uuid "bz1-p2"))
		(instances
			(project "VFBMS32"
				(path "/a2322edc-ff52-449c-92df-24faffac0236"
					(reference "BZ1")
					(unit 1)
				)
			)
		)
	)
	(symbol
		(lib_id "vfbms:AGM15T03LL")
		(at 85.0 245.0 0)
		(unit 1)
		(property "Reference" "Q_BZ1"
			(at 85.0 241.0 0)
			(effects (font (size 1.27 1.27)))
		)
		(property "Value" "2N7002 / AO3400A (Buzzer Switch)"
			(at 85.0 249.0 0)
			(effects (font (size 1.27 1.27)))
		)
		(property "Footprint" "Package_TO_SOT_SMD:SOT-23"
			(at 85.0 245.0 0)
			(hide yes)
			(effects (font (size 1.27 1.27)))
		)
		(pin "1" (uuid "qbz-p1"))
		(pin "2" (uuid "qbz-p2"))
		(pin "3" (uuid "qbz-p3"))
		(instances
			(project "VFBMS32"
				(path "/a2322edc-ff52-449c-92df-24faffac0236"
					(reference "Q_BZ1")
					(unit 1)
				)
			)
		)
	)"""

if '(property "Reference" "BZ1"' not in sch:
    last_paren = sch.rfind(')')
    sch = sch[:last_paren] + buzzer_instances + "\n)\n"

# Labels for buzzer connections
buzzer_labels = [
    '(label "PIN_BUZZER" (at 82.55 100.33 0) (fields_autoplaced yes) (effects (font (size 1.27 1.27)) (justify left)) (uuid "buzzer-gpio3-label"))',
    '(label "+3V3" (at 79.92 230.0 180) (fields_autoplaced yes) (effects (font (size 1.27 1.27)) (justify right)) (uuid "bz-pwr-label"))',
    '(label "BUZZ_LOW" (at 90.08 230.0 0) (fields_autoplaced yes) (effects (font (size 1.27 1.27)) (justify left)) (uuid "bz-low-label"))',
    '(label "PIN_BUZZER" (at 79.92 245.0 180) (fields_autoplaced yes) (effects (font (size 1.27 1.27)) (justify right)) (uuid "bz-gate-label"))',
    '(label "GND" (at 85.0 250.0 270) (fields_autoplaced yes) (effects (font (size 1.27 1.27)) (justify right)) (uuid "bz-gnd-label"))',
]

for lab in buzzer_labels:
    lab_name = re.search(r'label "([^"]+)"', lab).group(1)
    if f'label "{lab_name}"' not in sch or lab_name == "PIN_BUZZER":
        last_paren = sch.rfind(')')
        sch = sch[:last_paren] + "\t" + lab + "\n)\n"

with open(SCH_PATH, "w", encoding="utf-8") as f:
    f.write(sch)
print("Updated VFBMS32.kicad_sch with Buzzer and Drive Circuit!")

print("\n=== 2. UPDATING PCB LAYOUT WITH BUZZER (BZ1) & PASSIVES ===")
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
            if ref in ["BZ1", "Q_BZ1", "D_BZ1", "C_BZ1", "R_BZ_G", "R_BZ_PD", "L2"]:
                # Will replace / skip
                continue
            else:
                new_pcb_lines.append(fp_text)
    else:
        new_pcb_lines.append(line)

# Add BZ1, Q_BZ1, D_BZ1, C_BZ1, R_BZ_G, R_BZ_PD footprints
buzzer_footprints = """\t(footprint "vfbms:Buzzer_5.0x5.0mm_SMD"
		(layer "F.Cu")
		(uuid "bz1-uuid-001")
		(at 86.5 5.5)
		(descr "SMD Magnetic Buzzer 5.0x5.0mm 5030 Package (MLT-5030 / HY-5030)")
		(tags "Buzzer Beeper SMD 5030 5x5")
		(property "Reference" "BZ1"
			(at 0 -3.6 0)
			(layer "F.SilkS")
			(uuid "bz1-ref")
			(effects
				(font
					(size 0.7 0.7)
					(thickness 0.13)
				)
			)
		)
		(property "Value" "MLT-5030"
			(at 0 3.6 0)
			(layer "F.Fab")
			(uuid "bz1-val")
			(effects
				(font
					(size 0.8 0.8)
					(thickness 0.14)
				)
			)
		)
		(attr smd)
		(fp_rect
			(start -2.5 -2.5)
			(end 2.5 2.5)
			(stroke
				(width 0.12)
				(type solid)
			)
			(fill no)
			(layer "F.SilkS")
		)
		(fp_circle
			(center 0 0)
			(end 1.8 0)
			(stroke
				(width 0.15)
				(type solid)
			)
			(fill no)
			(layer "F.SilkS")
		)
		(fp_circle
			(center 0 0)
			(end 0.75 0)
			(stroke
				(width 0.15)
				(type solid)
			)
			(fill yes)
			(layer "F.SilkS")
		)
		(fp_text user "+"
			(at -1.8 -1.8 0)
			(layer "F.SilkS")
			(effects
				(font
					(size 0.8 0.8)
					(thickness 0.15)
				)
			)
		)
		(pad "1" smd rect
			(at -2.0 0 0)
			(size 1.5 2.2)
			(layers "F.Cu" "F.Paste" "F.Mask")
			(net 1 "+3V3")
			(uuid "bz1-pad1")
		)
		(pad "2" smd rect
			(at 2.0 0 0)
			(size 1.5 2.2)
			(layers "F.Cu" "F.Paste" "F.Mask")
			(net 10 "BUZZ_LOW")
			(uuid "bz1-pad2")
		)
		(model "${KICAD10_3DMODEL_DIR}/Buzzer_Beeper.3dshapes/PUIAudio_SMT_0825_S_4_R.step"
			(offset
				(xyz 0 0 0)
			)
			(scale
				(xyz 0.58 0.58 0.58)
			)
			(rotate
				(xyz 0 0 0)
			)
		)
	)
	(footprint "Capacitor_SMD:C_0603_1608Metric"
		(layer "F.Cu")
		(uuid "cbz1-uuid")
		(at 81.5 5.2 90)
		(descr "Capacitor SMD 0603 (1608 Metric)")
		(property "Reference" "C_BZ1"
			(at 0 -1.5 90)
			(layer "F.SilkS")
			(effects (font (size 0.6 0.6) (thickness 0.11)))
		)
		(property "Value" "1uF"
			(at 0 1.5 90)
			(layer "F.Fab")
			(effects (font (size 0.6 0.6) (thickness 0.11)))
		)
		(attr smd)
		(pad "1" smd roundrect (at -0.75 0 90) (size 0.8 0.8) (layers "F.Cu" "F.Paste" "F.Mask") (roundrect_rratio 0.25) (net 1 "+3V3"))
		(pad "2" smd roundrect (at 0.75 0 90) (size 0.8 0.8) (layers "F.Cu" "F.Paste" "F.Mask") (roundrect_rratio 0.25) (net 4 "GND"))
		(model "${KICAD10_3DMODEL_DIR}/Capacitor_SMD.3dshapes/C_0603_1608Metric.step"
			(offset (xyz 0 0 0)) (scale (xyz 1 1 1)) (rotate (xyz 0 0 0))
		)
	)
	(footprint "Diode_SMD:D_SOD-123"
		(layer "F.Cu")
		(uuid "dbz1-uuid")
		(at 91.5 5.2 90)
		(descr "Diode SOD-123")
		(property "Reference" "D_BZ1"
			(at 0 -1.8 90)
			(layer "F.SilkS")
			(effects (font (size 0.6 0.6) (thickness 0.11)))
		)
		(property "Value" "B0540W"
			(at 0 1.8 90)
			(layer "F.Fab")
			(effects (font (size 0.6 0.6) (thickness 0.11)))
		)
		(attr smd)
		(pad "1" smd rect (at -1.65 0 90) (size 0.9 1.2) (layers "F.Cu" "F.Paste" "F.Mask") (net 1 "+3V3"))
		(pad "2" smd rect (at 1.65 0 90) (size 0.9 1.2) (layers "F.Cu" "F.Paste" "F.Mask") (net 10 "BUZZ_LOW"))
		(model "${KICAD10_3DMODEL_DIR}/Diode_SMD.3dshapes/D_SOD-123.step"
			(offset (xyz 0 0 0)) (scale (xyz 1 1 1)) (rotate (xyz 0 0 0))
		)
	)
	(footprint "Package_TO_SOT_SMD:SOT-23"
		(layer "F.Cu")
		(uuid "qbz1-uuid")
		(at 86.5 9.5)
		(descr "SOT-23")
		(property "Reference" "Q_BZ1"
			(at 0 -2.2 0)
			(layer "F.SilkS")
			(effects (font (size 0.6 0.6) (thickness 0.11)))
		)
		(property "Value" "2N7002"
			(at 0 2.2 0)
			(layer "F.Fab")
			(effects (font (size 0.6 0.6) (thickness 0.11)))
		)
		(attr smd)
		(pad "1" smd rect (at -0.95 1.0 0) (size 0.8 0.9) (layers "F.Cu" "F.Paste" "F.Mask") (net 11 "PIN_BUZZER"))
		(pad "2" smd rect (at 0.95 1.0 0) (size 0.8 0.9) (layers "F.Cu" "F.Paste" "F.Mask") (net 4 "GND"))
		(pad "3" smd rect (at 0 -1.0 0) (size 0.8 0.9) (layers "F.Cu" "F.Paste" "F.Mask") (net 10 "BUZZ_LOW"))
		(model "${KICAD10_3DMODEL_DIR}/Package_TO_SOT_SMD.3dshapes/SOT-23.step"
			(offset (xyz 0 0 0)) (scale (xyz 1 1 1)) (rotate (xyz 0 0 0))
		)
	)
	(footprint "Resistor_SMD:R_0402_1005Metric"
		(layer "F.Cu")
		(uuid "rbzg-uuid")
		(at 84.0 9.5)
		(descr "Resistor SMD 0402 (1005 Metric)")
		(property "Reference" "R_BZ_G"
			(at 0 -1.2 0)
			(layer "F.SilkS")
			(effects (font (size 0.5 0.5) (thickness 0.10)))
		)
		(property "Value" "100R"
			(at 0 1.2 0)
			(layer "F.Fab")
			(effects (font (size 0.5 0.5) (thickness 0.10)))
		)
		(attr smd)
		(pad "1" smd roundrect (at -0.48 0 0) (size 0.56 0.62) (layers "F.Cu" "F.Paste" "F.Mask") (roundrect_rratio 0.25) (net 11 "PIN_BUZZER"))
		(pad "2" smd roundrect (at 0.48 0 0) (size 0.56 0.62) (layers "F.Cu" "F.Paste" "F.Mask") (roundrect_rratio 0.25) (net 11 "PIN_BUZZER"))
		(model "${KICAD10_3DMODEL_DIR}/Resistor_SMD.3dshapes/R_0402_1005Metric.step"
			(offset (xyz 0 0 0)) (scale (xyz 1 1 1)) (rotate (xyz 0 0 0))
		)
	)
	(footprint "Resistor_SMD:R_0402_1005Metric"
		(layer "F.Cu")
		(uuid "rbzpd-uuid")
		(at 89.0 9.5)
		(descr "Resistor SMD 0402 (1005 Metric)")
		(property "Reference" "R_BZ_PD"
			(at 0 -1.2 0)
			(layer "F.SilkS")
			(effects (font (size 0.5 0.5) (thickness 0.10)))
		)
		(property "Value" "10k"
			(at 0 1.2 0)
			(layer "F.Fab")
			(effects (font (size 0.5 0.5) (thickness 0.10)))
		)
		(attr smd)
		(pad "1" smd roundrect (at -0.48 0 0) (size 0.56 0.62) (layers "F.Cu" "F.Paste" "F.Mask") (roundrect_rratio 0.25) (net 11 "PIN_BUZZER"))
		(pad "2" smd roundrect (at 0.48 0 0) (size 0.56 0.62) (layers "F.Cu" "F.Paste" "F.Mask") (roundrect_rratio 0.25) (net 4 "GND"))
		(model "${KICAD10_3DMODEL_DIR}/Resistor_SMD.3dshapes/R_0402_1005Metric.step"
			(offset (xyz 0 0 0)) (scale (xyz 1 1 1)) (rotate (xyz 0 0 0))
		)
	)
"""

# Insert footprints before the final closing parenthesis
last_line_idx = len(new_pcb_lines) - 1
while last_line_idx >= 0 and ')' not in new_pcb_lines[last_line_idx]:
    last_line_idx -= 1

new_pcb_lines.insert(last_line_idx, buzzer_footprints)

with open(PCB_PATH, "w", encoding="utf-8") as f:
    f.writelines(new_pcb_lines)
print("Updated VFBMS32.kicad_pcb with Buzzer footprints successfully!")

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

# Detailed crops
im_top = Image.open(render_top)
bbox = im_top.getbbox()
if bbox:
    w = bbox[2] - bbox[0]
    h = bbox[3] - bbox[1]

    # Crop Buzzer & Power Stage Area (X ~ 45% to 75%)
    crop_bz_x1 = bbox[0] + int(w * 0.48)
    crop_bz_x2 = bbox[0] + int(w * 0.74)
    crop_y1 = max(0, bbox[1] - 20)
    crop_y2 = min(im_top.height, bbox[3] + 20)
    bz_zoom = im_top.crop((crop_bz_x1, crop_y1, crop_bz_x2, crop_y2))
    bz_zoom_path = os.path.join(PROJECT_DIR, "VFBMS32_buzzer_verified.png")
    bz_zoom.save(bz_zoom_path)
    print(f"Saved verified Buzzer section: {bz_zoom_path}")

    # Crop USB/ESP32/U7 Area (X ~ 65% to 100%)
    crop_usb_x1 = bbox[0] + int(w * 0.65)
    crop_usb_x2 = bbox[2] + 20
    esp_zoom = im_top.crop((crop_usb_x1, crop_y1, crop_usb_x2, crop_y2))
    esp_zoom_path = os.path.join(PROJECT_DIR, "VFBMS32_esp_usb_u7_verified.png")
    esp_zoom.save(esp_zoom_path)
    print(f"Saved verified USB/ESP/U7 section: {esp_zoom_path}")

# Export schematic PDF
sch_pdf = os.path.join(PROJECT_DIR, "VFBMS32_schematic.pdf")
subprocess.run([KICAD_CLI, "sch", "export", "pdf", "-o", sch_pdf, SCH_PATH], check=True)
print("Exported updated schematic PDF!")
print("ALL TASKS COMPLETED SUCCESSFULLY!")
