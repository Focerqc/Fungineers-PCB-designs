import uuid

sch_path = r"c:\Users\quinn\Documents\GitHub\Fungineers PCB designs\Q VFBMS32 AI PCB\VFBMS32.kicad_sch"
sym_path = r"C:\Program Files\KiCad\10.0\share\kicad\symbols\Device.kicad_sym"

with open(sch_path, "r", encoding="utf-8") as f:
    sch = f.read()

# 1. Read D_Schottky symbol definition from Device.kicad_sym
with open(sym_path, "r", encoding="utf-8") as f:
    dev_sym = f.read()

start_idx = dev_sym.find('(symbol "D_Schottky"')
# Find matching closing bracket
depth = 0
end_idx = start_idx
for i in range(start_idx, len(dev_sym)):
    if dev_sym[i] == '(':
        depth += 1
    elif dev_sym[i] == ')':
        depth -= 1
        if depth == 0:
            end_idx = i + 1
            break

d_schottky_def = dev_sym[start_idx:end_idx]
# Rename symbol name to "Device:D_Schottky" for lib_symbols inclusion
d_schottky_def = d_schottky_def.replace('(symbol "D_Schottky"', '(symbol "Device:D_Schottky"', 1)

# Check if Device:D_Schottky already in lib_symbols
if '(symbol "Device:D_Schottky"' not in sch:
    # insert before lib_symbols closing bracket
    lib_sym_close = sch.find('\n\t(sheet_instances')
    if lib_sym_close == -1:
        # find end of lib_symbols
        ls_start = sch.find('(lib_symbols')
        # find matching bracket for lib_symbols
        depth = 0
        for i in range(ls_start, len(sch)):
            if sch[i] == '(': depth += 1
            elif sch[i] == ')':
                depth -= 1
                if depth == 0:
                    lib_sym_close = i
                    break
    sch = sch[:lib_sym_close] + "\t\t" + d_schottky_def + "\n" + sch[lib_sym_close:]
    print("Added Device:D_Schottky to lib_symbols")

# Check if R_CHG1, D_CHG1, D_CHG2, D_CHG3 already in sch
instances_to_add = [
    ("R_CHG1", "100k", "Device:R", "Resistor_SMD:R_0603_1608Metric", 175.0, 105.0),
    ("D_CHG1", "DSK320", "Device:D_Schottky", "Diode_SMD:D_SOD-123F", 195.0, 105.0),
    ("D_CHG2", "DSK320", "Device:D_Schottky", "Diode_SMD:D_SOD-123F", 205.0, 105.0),
    ("D_CHG3", "DSK320", "Device:D_Schottky", "Diode_SMD:D_SOD-123F", 215.0, 105.0),
]

# Find root uuid
root_uuid = "a2322edc-ff52-449c-92df-24faffac0236"

new_symbols = []
for ref, val, lib_id, fp, x, y in instances_to_add:
    if f'(property "Reference" "{ref}"' in sch:
        print(f"{ref} already in schematic, skipping")
        continue
    u_sym = str(uuid.uuid4())
    u_p1 = str(uuid.uuid4())
    u_p2 = str(uuid.uuid4())
    sym_sexpr = f"""\t(symbol (lib_id "{lib_id}")
\t\t(at {x} {y} 0)
\t\t(unit 1)
\t\t(exclude_from_sim no)
\t\t(in_bom yes)
\t\t(on_board yes)
\t\t(dnp no)
\t\t(uuid "{u_sym}")
\t\t(property "Reference" "{ref}" (at {x} {y-4.0} 0) (effects (font (size 1.27 1.27))))
\t\t(property "Value" "{val}" (at {x} {y+4.0} 0) (effects (font (size 1.27 1.27))))
\t\t(property "Footprint" "{fp}" (at {x} {y} 0) (hide yes) (effects (font (size 1.27 1.27))))
\t\t(pin "1" (uuid "{u_p1}"))
\t\t(pin "2" (uuid "{u_p2}"))
\t\t(instances
\t\t\t(project "VFBMS32"
\t\t\t\t(path "/{root_uuid}" (reference "{ref}") (unit 1))
\t\t\t)
\t\t)
\t)
"""
    new_symbols.append(sym_sexpr)
    print(f"Prepared schematic symbol for {ref}")

# Insert before sheet_instances or final closing parenthesis
sheet_idx = sch.find('\n\t(sheet_instances')
if sheet_idx != -1:
    sch = sch[:sheet_idx] + "\n" + "".join(new_symbols) + sch[sheet_idx:]
else:
    last_paren = sch.rfind(')')
    sch = sch[:last_paren] + "\n" + "".join(new_symbols) + "\n)"

with open(sch_path, "w", encoding="utf-8") as f:
    f.write(sch)

print("VFBMS32.kicad_sch updated successfully!")
