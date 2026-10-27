import os

custom_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "qfbms.pretty")

# Female XT30PW-F Footprint:
# Solder lugs extend to +5.0 from center, pad size is 9.5 x 2.4 mm
# Roundrect ratio creates the rounded solder tab shape
fp_f_content = """(footprint "XT30PW-F_Lugs" (version 20240108) (generator pcbnew)
  (layer "F.Cu")
  (descr "AMASS XT30PW-F Right-Angle Female Connector with solder lugs")
  (tags "AMASS XT30 XT30PW-F")
  (attr through_hole)
  (fp_line (start -9.5 -5.2) (end 1.5 -5.2) (stroke (width 0.15) (type solid)) (layer "F.SilkS"))
  (fp_line (start 1.5 -5.2) (end 1.5 5.2) (stroke (width 0.15) (type solid)) (layer "F.SilkS"))
  (fp_line (start 1.5 5.2) (end -9.5 5.2) (stroke (width 0.15) (type solid)) (layer "F.SilkS"))
  (fp_line (start -9.5 5.2) (end -9.5 -5.2) (stroke (width 0.15) (type solid)) (layer "F.SilkS"))
  (fp_text reference "REF**" (at 0 -6.2) (layer "F.SilkS")
    (effects (font (size 1 1) (thickness 0.15)))
  )
  (fp_text value "XT30PW-F" (at 0 6.2) (layer "F.Fab")
    (effects (font (size 1 1) (thickness 0.15)))
  )
  (pad "1" thru_hole roundrect (at -0.5 -2.5) (size 9.5 2.5) (drill 1.4) (layers "*.Cu" "*.Mask") (roundrect_rratio 0.25))
  (pad "2" thru_hole roundrect (at -0.5 2.5) (size 9.5 2.5) (drill 1.4) (layers "*.Cu" "*.Mask") (roundrect_rratio 0.25))
  (model "${KIPRJMOD}/3dmodels/XT30PW-F.step"
    (offset (xyz 0.8 0 0))
    (scale (xyz 1 1 1))
    (rotate (xyz 0 0 90))
  )
)
"""

# Male XT30PW-M Footprint:
# Shorter solder lugs (7.5 x 2.5 mm) set back by 2mm compared to female
fp_m_content = """(footprint "XT30PW-M_Lugs" (version 20240108) (generator pcbnew)
  (layer "F.Cu")
  (descr "AMASS XT30PW-M Right-Angle Male Connector with recessed solder lugs")
  (tags "AMASS XT30 XT30PW-M")
  (attr through_hole)
  (fp_line (start -7.5 -5.2) (end 1.5 -5.2) (stroke (width 0.15) (type solid)) (layer "F.SilkS"))
  (fp_line (start 1.5 -5.2) (end 1.5 5.2) (stroke (width 0.15) (type solid)) (layer "F.SilkS"))
  (fp_line (start 1.5 5.2) (end -7.5 5.2) (stroke (width 0.15) (type solid)) (layer "F.SilkS"))
  (fp_line (start -7.5 5.2) (end -7.5 -5.2) (stroke (width 0.15) (type solid)) (layer "F.SilkS"))
  (fp_text reference "REF**" (at 0 -6.2) (layer "F.SilkS")
    (effects (font (size 1 1) (thickness 0.15)))
  )
  (fp_text value "XT30PW-M" (at 0 6.2) (layer "F.Fab")
    (effects (font (size 1 1) (thickness 0.15)))
  )
  (pad "2" thru_hole roundrect (at -0.5 -2.5) (size 7.5 2.5) (drill 1.4) (layers "*.Cu" "*.Mask") (roundrect_rratio 0.25))
  (pad "1" thru_hole roundrect (at -0.5 2.5) (size 7.5 2.5) (drill 1.4) (layers "*.Cu" "*.Mask") (roundrect_rratio 0.25))
  (model "${KIPRJMOD}/3dmodels/XT30PW-M.step"
    (offset (xyz 4.1 0 0))
    (scale (xyz 1 1 1))
    (rotate (xyz 0 0 90))
  )
)
"""

with open(os.path.join(custom_dir, "XT30PW-F_Lugs.kicad_mod"), "w") as f:
    f.write(fp_f_content)

with open(os.path.join(custom_dir, "XT30PW-M_Lugs.kicad_mod"), "w") as f:
    f.write(fp_m_content)

print("Footprints created successfully!")
