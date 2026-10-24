import os
import uuid
import re

pcb_dir = r"c:\Users\quinn\Documents\GitHub\Fungineers PCB designs\qfbms32 ai pcb"
pcb_path = os.path.join(pcb_dir, "qfbms32.kicad_pcb")

with open(pcb_path, "r", encoding="utf-8") as f:
    content = f.read()

def generate_0805_sexp(ref, val, x, y, rot=0.0):
    rot_str = f" {rot}" if rot != 0.0 else ""
    rot_prop = f" {rot}" if rot != 0.0 else " 0"
    return f"""\t(footprint "R_0805_2012Metric"
\t\t(layer "F.Cu")
\t\t(uuid "{uuid.uuid4()}")
\t\t(at {x} {y}{rot_str})
\t\t(descr "Resistor SMD 0805 (2012 Metric), square (rectangular) end terminal, IPC-7351 nominal, (Body size source: IPC-SM-782 page 72, https://www.pcb-3d.com/wordpress/wp-content/uploads/ipc-sm-782a_amendment_1_and_2.pdf)")
\t\t(tags "resistor")
\t\t(property "Reference" "{ref}"
\t\t\t(at 0 -1.65{rot_prop})
\t\t\t(layer "F.SilkS")
\t\t\t(hide yes)
\t\t\t(uuid "{uuid.uuid4()}")
\t\t\t(effects
\t\t\t\t(font
\t\t\t\t\t(size 1 1)
\t\t\t\t\t(thickness 0.15)
\t\t\t\t)
\t\t\t)
\t\t)
\t\t(property "Value" "{val}"
\t\t\t(at 0 1.65{rot_prop})
\t\t\t(layer "F.Fab")
\t\t\t(hide yes)
\t\t\t(uuid "{uuid.uuid4()}")
\t\t\t(effects
\t\t\t\t(font
\t\t\t\t\t(size 1 1)
\t\t\t\t\t(thickness 0.15)
\t\t\t\t)
\t\t\t)
\t\t)
\t\t(property "Datasheet" ""
\t\t\t(at 0 0{rot_prop})
\t\t\t(layer "F.Fab")
\t\t\t(hide yes)
\t\t\t(uuid "{uuid.uuid4()}")
\t\t\t(effects
\t\t\t\t(font
\t\t\t\t\t(size 1.27 1.27)
\t\t\t\t)
\t\t\t)
\t\t)
\t\t(property "Description" ""
\t\t\t(at 0 0{rot_prop})
\t\t\t(layer "F.Fab")
\t\t\t(hide yes)
\t\t\t(uuid "{uuid.uuid4()}")
\t\t\t(effects
\t\t\t\t(font
\t\t\t\t\t(size 1.27 1.27)
\t\t\t\t)
\t\t\t)
\t\t)
\t\t(property "KiLib_Generator" "SMD_2terminal_chip_molded"
\t\t\t(at 0 0{rot_prop})
\t\t\t(layer "F.SilkS")
\t\t\t(hide yes)
\t\t\t(uuid "{uuid.uuid4()}")
\t\t\t(effects
\t\t\t\t(font
\t\t\t\t\t(size 1 1)
\t\t\t\t\t(thickness 0.15)
\t\t\t\t)
\t\t\t)
\t\t)
\t\t(attr smd)
\t\t(duplicate_pad_numbers_are_jumpers no)
\t\t(fp_line
\t\t\t(start -0.227064 -0.735)
\t\t\t(end 0.227064 -0.735)
\t\t\t(stroke
\t\t\t\t(width 0.12)
\t\t\t\t(type solid)
\t\t\t)
\t\t\t(layer "F.SilkS")
\t\t\t(uuid "{uuid.uuid4()}")
\t\t)
\t\t(fp_line
\t\t\t(start -0.227064 0.735)
\t\t\t(end 0.227064 0.735)
\t\t\t(stroke
\t\t\t\t(width 0.12)
\t\t\t\t(type solid)
\t\t\t)
\t\t\t(layer "F.SilkS")
\t\t\t(uuid "{uuid.uuid4()}")
\t\t)
\t\t(fp_rect
\t\t\t(start -1.68 -0.95)
\t\t\t(end 1.68 0.95)
\t\t\t(stroke
\t\t\t\t(width 0.05)
\t\t\t\t(type solid)
\t\t\t)
\t\t\t(fill no)
\t\t\t(layer "F.CrtYd")
\t\t\t(uuid "{uuid.uuid4()}")
\t\t)
\t\t(fp_rect
\t\t\t(start -1 -0.625)
\t\t\t(end 1 0.625)
\t\t\t(stroke
\t\t\t\t(width 0.1)
\t\t\t\t(type solid)
\t\t\t)
\t\t\t(fill no)
\t\t\t(layer "F.Fab")
\t\t\t(uuid "{uuid.uuid4()}")
\t\t)
\t\t(fp_text user "${{REFERENCE}}"
\t\t\t(at 0 0{rot_prop})
\t\t\t(layer "F.Fab")
\t\t\t(uuid "{uuid.uuid4()}")
\t\t\t(effects
\t\t\t\t(font
\t\t\t\t\t(size 0.5 0.5)
\t\t\t\t\t(thickness 0.08)
\t\t\t\t)
\t\t\t)
\t\t)
\t\t(pad "1" smd roundrect
\t\t\t(at -0.9125 0)
\t\t\t(size 1.025 1.4)
\t\t\t(layers "F.Cu" "F.Mask" "F.Paste")
\t\t\t(roundrect_rratio 0.243902)
\t\t\t(uuid "{uuid.uuid4()}")
\t\t)
\t\t(pad "2" smd roundrect
\t\t\t(at 0.9125 0)
\t\t\t(size 1.025 1.4)
\t\t\t(layers "F.Cu" "F.Mask" "F.Paste")
\t\t\t(roundrect_rratio 0.243902)
\t\t\t(uuid "{uuid.uuid4()}")
\t\t)
\t\t(embedded_fonts no)
\t\t(model "${{KICAD10_3DMODEL_DIR}}/Resistor_SMD.3dshapes/R_0805_2012Metric.step"
\t\t\t(offset
\t\t\t\t(xyz 0 0 0)
\t\t\t)
\t\t\t(scale
\t\t\t\t(xyz 1 1 1)
\t\t\t)
\t\t\t(rotate
\t\t\t\t(xyz 0 0 0)
\t\t\t)
\t\t)
\t)"""

# Regex to match footprint block
# Pattern matches \t\(footprint[^\n]*\n(?:[^\n]*\n)*?\t\)
def replace_footprint(content, target_ref, new_sexp):
    lines = content.splitlines(keepends=True)
    out_lines = []
    in_target = False
    target_found = False
    fp_buf = []
    for line in lines:
        if line.startswith('\t(footprint '):
            fp_buf = [line]
        elif fp_buf:
            fp_buf.append(line)
            if line.startswith('\t)'):
                fp_text = "".join(fp_buf)
                if f'(property "Reference" "{target_ref}"' in fp_text:
                    out_lines.append(new_sexp + "\n")
                    target_found = True
                    print(f"Replaced footprint for {target_ref}")
                else:
                    out_lines.append(fp_text)
                fp_buf = []
        else:
            out_lines.append(line)
    if not target_found:
        print(f"Warning: footprint {target_ref} not found!")
    return "".join(out_lines)

# Box 1: X = 17.625 (or 17.63), Y = 15.00
new_s1 = generate_0805_sexp("R_S1", "1000", 17.63, 15.00, 0.0)
content = replace_footprint(content, "C_S1", new_s1)

# Box 2: X = 17.50, Y = 17.00
new_s2 = generate_0805_sexp("R_S2", "1000", 17.50, 17.00, 0.0)
content = replace_footprint(content, "C_S2", new_s2)

with open(pcb_path, "w", encoding="utf-8") as f:
    f.write(content)

print("Updated PCB written successfully.")
