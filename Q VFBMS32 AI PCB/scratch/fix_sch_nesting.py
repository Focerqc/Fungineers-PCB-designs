import re
import uuid

sch_path = r"c:\Users\quinn\Desktop\AI PCB CAD\Q VFBMS32 AI PCB\VFBMS32.kicad_sch"
with open(sch_path, "r", encoding="utf-8") as f:
    text = f.read()

# First, remove any appended content after the first closing paren of (kicad_sch ...)
# Let's find the proper structure of kicad_sch
# Find where (lib_symbols starts
lib_sym_start = text.find("(lib_symbols")
if lib_sym_start == -1:
    raise ValueError("Could not find (lib_symbols in schematic")

# Find the end of (lib_symbols ...)
depth = 0
lib_sym_end = -1
for i in range(lib_sym_start, len(text)):
    if text[i] == '(':
        depth += 1
    elif text[i] == ')':
        depth -= 1
        if depth == 0:
            lib_sym_end = i
            break

print(f"lib_symbols span: {lib_sym_start} to {lib_sym_end}")

# Clean any existing custom symbols or bad insertions
# Original symbols in lib_symbols:
# Battery_Management:BQ7695202PFB, MCU_Espressif:ESP32-C3, Regulator_Switching:TPS62130, Interface_CAN_LIN:SN65HVD230
# We can cleanly append custom symbols INSIDE (lib_symbols ...) right before lib_sym_end!

# Clean everything after (sheet_instances ...)
sheet_inst_idx = text.find("(sheet_instances")
sheet_inst_end = -1
if sheet_inst_idx != -1:
    depth = 0
    for i in range(sheet_inst_idx, len(text)):
        if text[i] == '(':
            depth += 1
        elif text[i] == ')':
            depth -= 1
            if depth == 0:
                sheet_inst_end = i
                break

print(f"sheet_instances span: {sheet_inst_idx} to {sheet_inst_end}")

# Rebuild clean base text without any rogue trailing text
clean_base = text[:sheet_inst_end+1] + "\n)\n"
# Ensure clean_base doesn't have duplicate closing parens
# Let's count depth
d = 0
cutoff = -1
for i, c in enumerate(clean_base):
    if c == '(':
        d += 1
    elif c == ')':
        d -= 1
        if d == 0:
            cutoff = i
            break
clean_base = clean_base[:cutoff+1] + "\n"

# Verify balance of clean_base
print(f"Clean base length: {len(clean_base)}, opens={clean_base.count('(')}, closes={clean_base.count(')')}")

toll_sym_def = '''\t\t(symbol "vfbms:AGM15T03LL"
\t\t\t(pin_names
\t\t\t\t(offset 1.016)
\t\t\t)
\t\t\t(exclude_from_sim no)
\t\t\t(in_bom yes)
\t\t\t(on_board yes)
\t\t\t(in_pos_files yes)
\t\t\t(property "Reference" "Q"
\t\t\t\t(at 5.08 1.27 0)
\t\t\t\t(effects
\t\t\t\t\t(font
\t\t\t\t\t\t(size 1.27 1.27)
\t\t\t\t\t)
\t\t\t\t\t(justify left)
\t\t\t\t)
\t\t\t)
\t\t\t(property "Value" "AGM15T03LL"
\t\t\t\t(at 5.08 -1.27 0)
\t\t\t\t(effects
\t\t\t\t\t(font
\t\t\t\t\t\t(size 1.27 1.27)
\t\t\t\t\t)
\t\t\t\t\t(justify left)
\t\t\t\t)
\t\t\t)
\t\t\t(property "Footprint" "vfbms:TOLL-8_AGM15T03LL"
\t\t\t\t(at 5.08 2.54 0)
\t\t\t\t(hide yes)
\t\t\t\t(effects
\t\t\t\t\t(font
\t\t\t\t\t\t(size 1.27 1.27)
\t\t\t\t\t)
\t\t\t\t)
\t\t\t)
\t\t\t(property "Datasheet" ""
\t\t\t\t(at 0 0 0)
\t\t\t\t(hide yes)
\t\t\t\t(effects
\t\t\t\t\t(font
\t\t\t\t\t\t(size 1.27 1.27)
\t\t\t\t\t)
\t\t\t\t)
\t\t\t)
\t\t\t(property "Description" "TOLL-8 N-Channel Power MOSFET 150V 300A"
\t\t\t\t(at 0 0 0)
\t\t\t\t(hide yes)
\t\t\t\t(effects
\t\t\t\t\t(font
\t\t\t\t\t\t(size 1.27 1.27)
\t\t\t\t\t)
\t\t\t\t)
\t\t\t)
\t\t\t(symbol "AGM15T03LL_1_1"
\t\t\t\t(rectangle
\t\t\t\t\t(start -5.08 6.35)
\t\t\t\t\t(end 5.08 -6.35)
\t\t\t\t\t(stroke
\t\t\t\t\t\t(width 0.254)
\t\t\t\t\t\t(type default)
\t\t\t\t\t)
\t\t\t\t\t(fill
\t\t\t\t\t\t(type background)
\t\t\t\t\t)
\t\t\t\t)
\t\t\t\t(pin input line
\t\t\t\t\t(at -7.62 0 0)
\t\t\t\t\t(length 2.54)
\t\t\t\t\t(name "G"
\t\t\t\t\t\t(effects
\t\t\t\t\t\t\t(font
\t\t\t\t\t\t\t\t(size 1.27 1.27)
\t\t\t\t\t\t\t)
\t\t\t\t\t\t)
\t\t\t\t\t)
\t\t\t\t\t(number "1"
\t\t\t\t\t\t(effects
\t\t\t\t\t\t\t(font
\t\t\t\t\t\t\t\t(size 1.27 1.27)
\t\t\t\t\t\t\t)
\t\t\t\t\t\t)
\t\t\t\t\t)
\t\t\t\t)
\t\t\t\t(pin passive line
\t\t\t\t\t(at 0 8.89 270)
\t\t\t\t\t(length 2.54)
\t\t\t\t\t(name "D"
\t\t\t\t\t\t(effects
\t\t\t\t\t\t\t(font
\t\t\t\t\t\t\t\t(size 1.27 1.27)
\t\t\t\t\t\t\t)
\t\t\t\t\t\t)
\t\t\t\t\t)
\t\t\t\t\t(number "D"
\t\t\t\t\t\t(effects
\t\t\t\t\t\t\t(font
\t\t\t\t\t\t\t\t(size 1.27 1.27)
\t\t\t\t\t\t\t)
\t\t\t\t\t\t)
\t\t\t\t\t)
\t\t\t\t)
\t\t\t\t(pin passive line
\t\t\t\t\t(at 0 -8.89 90)
\t\t\t\t\t(length 2.54)
\t\t\t\t\t(name "S"
\t\t\t\t\t\t(effects
\t\t\t\t\t\t\t(font
\t\t\t\t\t\t\t\t(size 1.27 1.27)
\t\t\t\t\t\t\t)
\t\t\t\t\t\t)
\t\t\t\t\t)
\t\t\t\t\t(number "2"
\t\t\t\t\t\t(effects
\t\t\t\t\t\t\t(font
\t\t\t\t\t\t\t\t(size 1.27 1.27)
\t\t\t\t\t\t\t)
\t\t\t\t\t\t)
\t\t\t\t\t)
\t\t\t\t)
\t\t\t)
\t\t)\n'''

ssr_sym_def = '''\t\t(symbol "vfbms:H2440_SSR"
\t\t\t(pin_names
\t\t\t\t(offset 1.016)
\t\t\t)
\t\t\t(exclude_from_sim no)
\t\t\t(in_bom yes)
\t\t\t(on_board yes)
\t\t\t(in_pos_files yes)
\t\t\t(property "Reference" "U"
\t\t\t\t(at 0 10.16 0)
\t\t\t\t(effects
\t\t\t\t\t(font
\t\t\t\t\t\t(size 1.27 1.27)
\t\t\t\t\t)
\t\t\t\t)
\t\t\t)
\t\t\t(property "Value" "H2440_SSR"
\t\t\t\t(at 0 7.62 0)
\t\t\t\t(effects
\t\t\t\t\t(font
\t\t\t\t\t\t(size 1.27 1.27)
\t\t\t\t\t)
\t\t\t\t)
\t\t\t)
\t\t\t(property "Footprint" "Package_SO:SOIC-8_3.9x4.9mm_P1.27mm"
\t\t\t\t(at 0 5.08 0)
\t\t\t\t(hide yes)
\t\t\t\t(effects
\t\t\t\t\t(font
\t\t\t\t\t\t(size 1.27 1.27)
\t\t\t\t\t)
\t\t\t\t)
\t\t\t)
\t\t\t(symbol "H2440_SSR_1_1"
\t\t\t\t(rectangle
\t\t\t\t\t(start -7.62 6.35)
\t\t\t\t\t(end 7.62 -6.35)
\t\t\t\t\t(stroke
\t\t\t\t\t\t(width 0.254)
\t\t\t\t\t\t(type default)
\t\t\t\t\t)
\t\t\t\t\t(fill
\t\t\t\t\t\t(type background)
\t\t\t\t\t)
\t\t\t\t)
\t\t\t\t(pin input line
\t\t\t\t\t(at -10.16 3.81 0)
\t\t\t\t\t(length 2.54)
\t\t\t\t\t(name "IN_CHG"
\t\t\t\t\t\t(effects (font (size 1.27 1.27)))
\t\t\t\t\t)
\t\t\t\t\t(number "1"
\t\t\t\t\t\t(effects (font (size 1.27 1.27)))
\t\t\t\t\t)
\t\t\t\t)
\t\t\t\t(pin input line
\t\t\t\t\t(at -10.16 1.27 0)
\t\t\t\t\t(length 2.54)
\t\t\t\t\t(name "IN_DSG"
\t\t\t\t\t\t(effects (font (size 1.27 1.27)))
\t\t\t\t\t)
\t\t\t\t\t(number "2"
\t\t\t\t\t\t(effects (font (size 1.27 1.27)))
\t\t\t\t\t)
\t\t\t\t)
\t\t\t\t(pin input line
\t\t\t\t\t(at -10.16 -1.27 0)
\t\t\t\t\t(length 2.54)
\t\t\t\t\t(name "PSW_EN"
\t\t\t\t\t\t(effects (font (size 1.27 1.27)))
\t\t\t\t\t)
\t\t\t\t\t(number "3"
\t\t\t\t\t\t(effects (font (size 1.27 1.27)))
\t\t\t\t\t)
\t\t\t\t)
\t\t\t\t(pin power_in line
\t\t\t\t\t(at -10.16 -3.81 0)
\t\t\t\t\t(length 2.54)
\t\t\t\t\t(name "GND"
\t\t\t\t\t\t(effects (font (size 1.27 1.27)))
\t\t\t\t\t)
\t\t\t\t\t(number "4"
\t\t\t\t\t\t(effects (font (size 1.27 1.27)))
\t\t\t\t\t)
\t\t\t\t)
\t\t\t\t(pin output line
\t\t\t\t\t(at 10.16 3.81 180)
\t\t\t\t\t(length 2.54)
\t\t\t\t\t(name "OUT_CHG"
\t\t\t\t\t\t(effects (font (size 1.27 1.27)))
\t\t\t\t\t)
\t\t\t\t\t(number "8"
\t\t\t\t\t\t(effects (font (size 1.27 1.27)))
\t\t\t\t\t)
\t\t\t\t)
\t\t\t\t(pin output line
\t\t\t\t\t(at 10.16 1.27 180)
\t\t\t\t\t(length 2.54)
\t\t\t\t\t(name "OUT_DSG"
\t\t\t\t\t\t(effects (font (size 1.27 1.27)))
\t\t\t\t\t)
\t\t\t\t\t(number "7"
\t\t\t\t\t\t(effects (font (size 1.27 1.27)))
\t\t\t\t\t)
\t\t\t\t)
\t\t\t\t(pin passive line
\t\t\t\t\t(at 10.16 -1.27 180)
\t\t\t\t\t(length 2.54)
\t\t\t\t\t(name "VBAT_S"
\t\t\t\t\t\t(effects (font (size 1.27 1.27)))
\t\t\t\t\t)
\t\t\t\t\t(number "6"
\t\t\t\t\t\t(effects (font (size 1.27 1.27)))
\t\t\t\t\t)
\t\t\t\t)
\t\t\t\t(pin power_in line
\t\t\t\t\t(at 10.16 -3.81 180)
\t\t\t\t\t(length 2.54)
\t\t\t\t\t(name "VBOOST"
\t\t\t\t\t\t(effects (font (size 1.27 1.27)))
\t\t\t\t\t)
\t\t\t\t\t(number "5"
\t\t\t\t\t\t(effects (font (size 1.27 1.27)))
\t\t\t\t\t)
\t\t\t\t)
\t\t\t)
\t\t)\n'''

res_sym_def = '''\t\t(symbol "Device:R"
\t\t\t(pin_numbers (hide yes))
\t\t\t(pin_names (offset 0) (hide yes))
\t\t\t(exclude_from_sim no)
\t\t\t(in_bom yes)
\t\t\t(on_board yes)
\t\t\t(in_pos_files yes)
\t\t\t(property "Reference" "R"
\t\t\t\t(at 2.032 0 90)
\t\t\t\t(effects (font (size 1.27 1.27)))
\t\t\t)
\t\t\t(property "Value" "R"
\t\t\t\t(at -2.032 0 90)
\t\t\t\t(effects (font (size 1.27 1.27)))
\t\t\t)
\t\t\t(property "Footprint" "Resistor_SMD:R_0603_1608Metric"
\t\t\t\t(at 0 0 90)
\t\t\t\t(hide yes)
\t\t\t\t(effects (font (size 1.27 1.27)))
\t\t\t)
\t\t\t(symbol "R_1_1"
\t\t\t\t(rectangle
\t\t\t\t\t(start -1.016 2.54)
\t\t\t\t\t(end 1.016 -2.54)
\t\t\t\t\t(stroke (width 0.254) (type default))
\t\t\t\t\t(fill (type none))
\t\t\t\t)
\t\t\t\t(pin passive line
\t\t\t\t\t(at 0 3.81 270)
\t\t\t\t\t(length 1.27)
\t\t\t\t\t(name "~" (effects (font (size 1.27 1.27))))
\t\t\t\t\t(number "1" (effects (font (size 1.27 1.27))))
\t\t\t\t)
\t\t\t\t(pin passive line
\t\t\t\t\t(at 0 -3.81 90)
\t\t\t\t\t(length 1.27)
\t\t\t\t\t(name "~" (effects (font (size 1.27 1.27))))
\t\t\t\t\t(number "2" (effects (font (size 1.27 1.27))))
\t\t\t\t)
\t\t\t)
\t\t)\n'''

# Recompute lib_sym_end on clean_base
lib_sym_start = clean_base.find("(lib_symbols")
depth = 0
lib_sym_end = -1
for i in range(lib_sym_start, len(clean_base)):
    if clean_base[i] == '(':
        depth += 1
    elif clean_base[i] == ')':
        depth -= 1
        if depth == 0:
            lib_sym_end = i
            break

# Insert inside lib_symbols right before the closing paren of (lib_symbols ...)
base_with_libs = clean_base[:lib_sym_end] + toll_sym_def + ssr_sym_def + res_sym_def + clean_base[lib_sym_end:]

# Now insert instances and labels right before (sheet_instances
sheet_idx = base_with_libs.find("(sheet_instances")

instantiations = f'''\t(symbol (lib_id "vfbms:AGM15T03LL")
\t\t(at 195.0 45.0 0)
\t\t(unit 1)
\t\t(exclude_from_sim no)
\t\t(in_bom yes)
\t\t(on_board yes)
\t\t(dnp no)
\t\t(uuid "{uuid.uuid4()}")
\t\t(property "Reference" "Q1" (at 195.0 35.0 0) (effects (font (size 1.27 1.27))))
\t\t(property "Value" "AGM15T03LL (CHG FET)" (at 195.0 37.5 0) (effects (font (size 1.27 1.27))))
\t\t(property "Footprint" "vfbms:TOLL-8_AGM15T03LL" (at 195.0 33.0 0) (hide yes) (effects (font (size 1.27 1.27))))
\t\t(pin "1" (uuid "{uuid.uuid4()}"))
\t\t(pin "D" (uuid "{uuid.uuid4()}"))
\t\t(pin "2" (uuid "{uuid.uuid4()}"))
\t\t(instances
\t\t\t(project "VFBMS32"
\t\t\t\t(path "/a2322edc-ff52-449c-92df-24faffac0236" (reference "Q1") (unit 1))
\t\t\t)
\t\t)
\t)

\t(symbol (lib_id "vfbms:AGM15T03LL")
\t\t(at 195.0 80.0 0)
\t\t(unit 1)
\t\t(exclude_from_sim no)
\t\t(in_bom yes)
\t\t(on_board yes)
\t\t(dnp no)
\t\t(uuid "{uuid.uuid4()}")
\t\t(property "Reference" "Q2" (at 195.0 70.0 0) (effects (font (size 1.27 1.27))))
\t\t(property "Value" "AGM15T03LL (DSG FET)" (at 195.0 72.5 0) (effects (font (size 1.27 1.27))))
\t\t(property "Footprint" "vfbms:TOLL-8_AGM15T03LL" (at 195.0 68.0 0) (hide yes) (effects (font (size 1.27 1.27))))
\t\t(pin "1" (uuid "{uuid.uuid4()}"))
\t\t(pin "D" (uuid "{uuid.uuid4()}"))
\t\t(pin "2" (uuid "{uuid.uuid4()}"))
\t\t(instances
\t\t\t(project "VFBMS32"
\t\t\t\t(path "/a2322edc-ff52-449c-92df-24faffac0236" (reference "Q2") (unit 1))
\t\t\t)
\t\t)
\t)

\t(symbol (lib_id "vfbms:H2440_SSR")
\t\t(at 155.0 60.0 0)
\t\t(unit 1)
\t\t(exclude_from_sim no)
\t\t(in_bom yes)
\t\t(on_board yes)
\t\t(dnp no)
\t\t(uuid "{uuid.uuid4()}")
\t\t(property "Reference" "U_SSR1" (at 155.0 50.0 0) (effects (font (size 1.27 1.27))))
\t\t(property "Value" "H2440_SSR" (at 155.0 52.5 0) (effects (font (size 1.27 1.27))))
\t\t(property "Footprint" "Package_SO:SOIC-8_3.9x4.9mm_P1.27mm" (at 155.0 48.0 0) (hide yes) (effects (font (size 1.27 1.27))))
\t\t(pin "1" (uuid "{uuid.uuid4()}"))
\t\t(pin "2" (uuid "{uuid.uuid4()}"))
\t\t(pin "3" (uuid "{uuid.uuid4()}"))
\t\t(pin "4" (uuid "{uuid.uuid4()}"))
\t\t(pin "5" (uuid "{uuid.uuid4()}"))
\t\t(pin "6" (uuid "{uuid.uuid4()}"))
\t\t(pin "7" (uuid "{uuid.uuid4()}"))
\t\t(pin "8" (uuid "{uuid.uuid4()}"))
\t\t(instances
\t\t\t(project "VFBMS32"
\t\t\t\t(path "/a2322edc-ff52-449c-92df-24faffac0236" (reference "U_SSR1") (unit 1))
\t\t\t)
\t\t)
\t)

\t(symbol (lib_id "Device:R")
\t\t(at 175.0 45.0 90)
\t\t(unit 1)
\t\t(exclude_from_sim no)
\t\t(in_bom yes)
\t\t(on_board yes)
\t\t(dnp no)
\t\t(uuid "{uuid.uuid4()}")
\t\t(property "Reference" "R_G1" (at 175.0 41.0 0) (effects (font (size 1.27 1.27))))
\t\t(property "Value" "100R" (at 175.0 48.0 0) (effects (font (size 1.27 1.27))))
\t\t(property "Footprint" "Resistor_SMD:R_0603_1608Metric" (at 175.0 45.0 0) (hide yes) (effects (font (size 1.27 1.27))))
\t\t(pin "1" (uuid "{uuid.uuid4()}"))
\t\t(pin "2" (uuid "{uuid.uuid4()}"))
\t\t(instances
\t\t\t(project "VFBMS32"
\t\t\t\t(path "/a2322edc-ff52-449c-92df-24faffac0236" (reference "R_G1") (unit 1))
\t\t\t)
\t\t)
\t)

\t(symbol (lib_id "Device:R")
\t\t(at 175.0 80.0 90)
\t\t(unit 1)
\t\t(exclude_from_sim no)
\t\t(in_bom yes)
\t\t(on_board yes)
\t\t(dnp no)
\t\t(uuid "{uuid.uuid4()}")
\t\t(property "Reference" "R_G2" (at 175.0 76.0 0) (effects (font (size 1.27 1.27))))
\t\t(property "Value" "100R" (at 175.0 83.0 0) (effects (font (size 1.27 1.27))))
\t\t(property "Footprint" "Resistor_SMD:R_0603_1608Metric" (at 175.0 80.0 0) (hide yes) (effects (font (size 1.27 1.27))))
\t\t(pin "1" (uuid "{uuid.uuid4()}"))
\t\t(pin "2" (uuid "{uuid.uuid4()}"))
\t\t(instances
\t\t\t(project "VFBMS32"
\t\t\t\t(path "/a2322edc-ff52-449c-92df-24faffac0236" (reference "R_G2") (unit 1))
\t\t\t)
\t\t)
\t)

\t(label "PIN_CHG_EN"
\t\t(at 140.0 63.81 180)
\t\t(effects (font (size 1.27 1.27)) (justify right bottom))
\t\t(uuid "{uuid.uuid4()}")
\t)
\t(label "PIN_OUT_EN"
\t\t(at 140.0 61.27 180)
\t\t(effects (font (size 1.27 1.27)) (justify right bottom))
\t\t(uuid "{uuid.uuid4()}")
\t)
\t(label "PIN_PSW_EN"
\t\t(at 140.0 58.73 180)
\t\t(effects (font (size 1.27 1.27)) (justify right bottom))
\t\t(uuid "{uuid.uuid4()}")
\t)
\t(label "Q1_GATE"
\t\t(at 187.38 45.0 0)
\t\t(effects (font (size 1.27 1.27)) (justify left bottom))
\t\t(uuid "{uuid.uuid4()}")
\t)
\t(label "Q2_GATE"
\t\t(at 187.38 80.0 0)
\t\t(effects (font (size 1.27 1.27)) (justify left bottom))
\t\t(uuid "{uuid.uuid4()}")
\t)
\t(label "CHG+"
\t\t(at 195.0 36.11 90)
\t\t(effects (font (size 1.27 1.27)) (justify left bottom))
\t\t(uuid "{uuid.uuid4()}")
\t)
\t(label "BAT+"
\t\t(at 195.0 71.11 90)
\t\t(effects (font (size 1.27 1.27)) (justify left bottom))
\t\t(uuid "{uuid.uuid4()}")
\t)
\t(label "PACK_RAIL"
\t\t(at 195.0 53.89 270)
\t\t(effects (font (size 1.27 1.27)) (justify right bottom))
\t\t(uuid "{uuid.uuid4()}")
\t)
\t(label "PIN_CHG_EN"
\t\t(at 66.0 116.586 0)
\t\t(effects (font (size 1.27 1.27)) (justify left bottom))
\t\t(uuid "{uuid.uuid4()}")
\t)
\t(label "PIN_OUT_EN"
\t\t(at 66.0 114.046 0)
\t\t(effects (font (size 1.27 1.27)) (justify left bottom))
\t\t(uuid "{uuid.uuid4()}")
\t)
\t(label "PIN_PSW_EN"
\t\t(at 18.0 134.366 180)
\t\t(effects (font (size 1.27 1.27)) (justify right bottom))
\t\t(uuid "{uuid.uuid4()}")
\t)
\t(label "PIN_PCHG_EN"
\t\t(at 18.0 139.446 180)
\t\t(effects (font (size 1.27 1.27)) (justify right bottom))
\t\t(uuid "{uuid.uuid4()}")
\t)
\t(label "PIN_COM_EN"
\t\t(at 18.0 136.906 180)
\t\t(effects (font (size 1.27 1.27)) (justify right bottom))
\t\t(uuid "{uuid.uuid4()}")
\t)
\t(label "PIN_ENABLE"
\t\t(at 18.0 103.886 180)
\t\t(effects (font (size 1.27 1.27)) (justify right bottom))
\t\t(uuid "{uuid.uuid4()}")
\t)
\t(label "CAN_RX"
\t\t(at 66.0 119.126 0)
\t\t(effects (font (size 1.27 1.27)) (justify left bottom))
\t\t(uuid "{uuid.uuid4()}")
\t)
\t(label "CAN_TX"
\t\t(at 66.0 121.666 0)
\t\t(effects (font (size 1.27 1.27)) (justify left bottom))
\t\t(uuid "{uuid.uuid4()}")
\t)\n'''

final_sch = base_with_libs[:sheet_idx] + instantiations + base_with_libs[sheet_idx:]

with open(sch_path, "w", encoding="utf-8") as f:
    f.write(final_sch)

print("Rewrote VFBMS32.kicad_sch cleanly with exact structure!")
