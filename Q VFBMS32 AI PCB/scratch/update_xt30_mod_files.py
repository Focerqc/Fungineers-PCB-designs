import os

custom_dir = r"c:\Users\quinn\Desktop\AI PCB CAD\Q VFBMS32 AI PCB\vfbms.pretty"

# Female XT30PW-F Footprint:
# Pins at X = +8.742, Y = +/- 2.500
# Mounting tabs at X = +3.742, Y = +/- 5.500
fp_f_content = """(footprint "XT30PW-F_Lugs" (version 20240108) (generator pcbnew)
  (layer "F.Cu")
  (descr "AMASS XT30PW-F Right-Angle Female Connector with PTH pins and mounting tabs")
  (tags "AMASS XT30 XT30PW-F")
  (attr through_hole)
  (fp_line (start -5.2 -5.5) (end 5.5 -5.5) (stroke (width 0.15) (type solid)) (layer "F.SilkS"))
  (fp_line (start 5.5 -5.5) (end 5.5 5.5) (stroke (width 0.15) (type solid)) (layer "F.SilkS"))
  (fp_line (start 5.5 5.5) (end -5.2 5.5) (stroke (width 0.15) (type solid)) (layer "F.SilkS"))
  (fp_line (start -5.2 5.5) (end -5.2 -5.5) (stroke (width 0.15) (type solid)) (layer "F.SilkS"))
  (fp_text reference "REF**" (at 2.0 -7.0) (layer "F.SilkS")
    (effects (font (size 1 1) (thickness 0.15)))
  )
  (fp_text value "XT30PW-F" (at 2.0 7.0) (layer "F.Fab")
    (effects (font (size 1 1) (thickness 0.15)))
  )
  (pad "1" thru_hole circle (at 8.742 -2.5) (size 2.8 2.8) (drill 1.6) (layers "*.Cu" "*.Mask"))
  (pad "2" thru_hole circle (at 8.742 2.5) (size 2.8 2.8) (drill 1.6) (layers "*.Cu" "*.Mask"))
  (pad "TAB1" thru_hole circle (at 3.742 -5.5) (size 2.4 2.4) (drill 1.3) (layers "*.Cu" "*.Mask"))
  (pad "TAB2" thru_hole circle (at 3.742 5.5) (size 2.4 2.4) (drill 1.3) (layers "*.Cu" "*.Mask"))
  (model "${KIPRJMOD}/3dmodels/XT30PW-F.step"
    (offset (xyz 0.8 0 0))
    (scale (xyz 1 1 1))
    (rotate (xyz 0 0 90))
  )
)
"""

# Male XT30PW-M Footprint:
# Pins at X = +8.100, Y = +/- 2.500
# Mounting tabs at X = -1.800, Y = +/- 5.600
# 3D model Z-offset = +2.5 to sit flush on top copper layer!
fp_m_content = """(footprint "XT30PW-M_Lugs" (version 20240108) (generator pcbnew)
  (layer "F.Cu")
  (descr "AMASS XT30PW-M Right-Angle Male Connector with PTH pins and mounting tabs")
  (tags "AMASS XT30 XT30PW-M")
  (attr through_hole)
  (fp_line (start -4.0 -5.6) (end 5.5 -5.6) (stroke (width 0.15) (type solid)) (layer "F.SilkS"))
  (fp_line (start 5.5 -5.6) (end 5.5 5.6) (stroke (width 0.15) (type solid)) (layer "F.SilkS"))
  (fp_line (start 5.5 5.6) (end -4.0 5.6) (stroke (width 0.15) (type solid)) (layer "F.SilkS"))
  (fp_line (start -4.0 5.6) (end -4.0 -5.6) (stroke (width 0.15) (type solid)) (layer "F.SilkS"))
  (fp_text reference "REF**" (at 2.0 -7.0) (layer "F.SilkS")
    (effects (font (size 1 1) (thickness 0.15)))
  )
  (fp_text value "XT30PW-M" (at 2.0 7.0) (layer "F.Fab")
    (effects (font (size 1 1) (thickness 0.15)))
  )
  (pad "2" thru_hole circle (at 8.1 -2.5) (size 2.8 2.8) (drill 1.6) (layers "*.Cu" "*.Mask"))
  (pad "1" thru_hole circle (at 8.1 2.5) (size 2.8 2.8) (drill 1.6) (layers "*.Cu" "*.Mask"))
  (pad "TAB1" thru_hole circle (at -1.8 -5.6) (size 2.4 2.4) (drill 1.3) (layers "*.Cu" "*.Mask"))
  (pad "TAB2" thru_hole circle (at -1.8 5.6) (size 2.4 2.4) (drill 1.3) (layers "*.Cu" "*.Mask"))
  (model "${KIPRJMOD}/3dmodels/XT30PW-M.step"
    (offset (xyz 4.1 0 2.5))
    (scale (xyz 1 1 1))
    (rotate (xyz 0 0 90))
  )
)
"""

with open(os.path.join(custom_dir, "XT30PW-F_Lugs.kicad_mod"), "w") as f:
    f.write(fp_f_content)

with open(os.path.join(custom_dir, "XT30PW-M_Lugs.kicad_mod"), "w") as f:
    f.write(fp_m_content)

print("Updated footprints saved to vfbms.pretty!")
