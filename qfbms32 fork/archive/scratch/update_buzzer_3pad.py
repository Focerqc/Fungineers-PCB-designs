"""
Generate true 3-pad FUET-5030 SMD Buzzer footprint matching measured boxes:
Pad 1 (Top-Right):    center = (90.05, 1.10), size = 1.00 x 1.60 mm
Pad 2 (Bottom-Right): center = (90.08, 4.53), size = 0.85 x 1.55 mm
Pad 3 (Bottom-Left):  center = (86.55, 4.47), size = 0.80 x 1.45 mm

Component body center: (88.30, 2.80)
Body size: 5.0 x 5.0 mm (from X=85.80 to 90.80, Y=0.30 to 5.30)
"""
import os

mod_dir = r"c:\Users\quinn\Documents\GitHub\Fungineers PCB designs\Q VFBMS32 AI PCB\vfbms.pretty"
fp_path = os.path.join(mod_dir, "Buzzer_5.0x5.0mm_SMD.kicad_mod")

# Pad offsets relative to body center (88.30, 2.80):
# Pad 1: (90.05 - 88.30, 1.10 - 2.80) = (+1.75, -1.70)
# Pad 2: (90.08 - 88.30, 4.53 - 2.80) = (+1.78, +1.73)
# Pad 3: (86.55 - 88.30, 4.47 - 2.80) = (-1.75, +1.67)

content = """(footprint "Buzzer_5.0x5.0mm_SMD"
\t(version 20260206)
\t(generator "kicad-footprint-generator")
\t(layer "F.Cu")
\t(descr "SMD Magnetic Buzzer 5.0x5.0mm 3-pad Package (FUET-5030 / MLT-5030)")
\t(tags "Buzzer Beeper SMD 5030 5x5 FUET")
\t(property "Reference" "REF**"
\t\t(at 0 -3.6 0)
\t\t(layer "F.SilkS")
\t\t(effects
\t\t\t(font
\t\t\t\t(size 0.7 0.7)
\t\t\t\t(thickness 0.13)
\t\t\t)
\t\t)
\t)
\t(property "Value" "Buzzer_5.0x5.0mm_SMD"
\t\t(at 0 3.6 0)
\t\t(layer "F.Fab")
\t\t(effects
\t\t\t(font
\t\t\t\t(size 0.8 0.8)
\t\t\t\t(thickness 0.14)
\t\t\t)
\t\t)
\t)
\t(property "Footprint" "vfbms:Buzzer_5.0x5.0mm_SMD"
\t\t(at 0 0 0)
\t\t(layer "F.Fab")
\t\t(hide yes)
\t\t(effects
\t\t\t(font
\t\t\t\t(size 1.27 1.27)
\t\t\t)
\t\t)
\t)
\t(attr smd)
\t(fp_rect
\t\t(start -2.5 -2.5)
\t\t(end 2.5 2.5)
\t\t(stroke
\t\t\t(width 0.1)
\t\t\t(type solid)
\t\t)
\t\t(fill no)
\t\t(layer "F.Fab")
\t)
\t(fp_rect
\t\t(start -2.7 -2.7)
\t\t(end 2.7 2.7)
\t\t(stroke
\t\t\t(width 0.05)
\t\t\t(type solid)
\t\t)
\t\t(fill no)
\t\t(layer "F.CrtYd")
\t)
\t(fp_rect
\t\t(start -2.5 -2.5)
\t\t(end 2.5 2.5)
\t\t(stroke
\t\t\t(width 0.12)
\t\t\t(type solid)
\t\t)
\t\t(fill no)
\t\t(layer "F.SilkS")
\t)
\t(fp_circle
\t\t(center 0 0)
\t\t(end 1.8 0)
\t\t(stroke
\t\t\t(width 0.15)
\t\t\t(type solid)
\t\t)
\t\t(fill no)
\t\t(layer "F.SilkS")
\t)
\t(fp_circle
\t\t(center 0 0)
\t\t(end 0.75 0)
\t\t(stroke
\t\t\t(width 0.15)
\t\t\t(type solid)
\t\t)
\t\t(fill yes)
\t\t(layer "F.SilkS")
\t)
\t(fp_poly
\t\t(pts
\t\t\t(xy -2.5 -2.5)
\t\t\t(xy -1.2 -2.5)
\t\t\t(xy -2.5 -1.2)
\t\t)
\t\t(stroke
\t\t\t(width 0.12)
\t\t\t(type solid)
\t\t)
\t\t(fill solid)
\t\t(layer "F.SilkS")
\t)
\t(pad "1" smd rect
\t\t(at 1.75 -1.70 0)
\t\t(size 1.00 1.60)
\t\t(layers "F.Cu" "F.Paste" "F.Mask")
\t)
\t(pad "2" smd rect
\t\t(at 1.78 1.73 0)
\t\t(size 0.85 1.55)
\t\t(layers "F.Cu" "F.Paste" "F.Mask")
\t)
\t(pad "3" smd rect
\t\t(at -1.75 1.67 0)
\t\t(size 0.80 1.45)
\t\t(layers "F.Cu" "F.Paste" "F.Mask")
\t)
\t(model "${KICAD10_3DMODEL_DIR}/Buzzer_Beeper.3dshapes/PUIAudio_SMT_0825_S_4_R.step"
\t\t(offset
\t\t\t(xyz 0 0 0)
\t\t)
\t\t(scale
\t\t\t(xyz 0.58 0.58 0.58)
\t\t)
\t\t(rotate
\t\t\t(xyz 0 0 0)
\t\t)
\t)
)
"""

with open(fp_path, "w", encoding="utf-8") as f:
    f.write(content)
print("Updated footprint to 3-pad FUET-5030:", fp_path)
