"""Add C_FLT1 (Device:C) and R_B33 (Device:R) symbols to VFBMS32.kicad_sch."""
import os, shutil, datetime

proj = r"c:\Users\quinn\Documents\GitHub\Fungineers PCB designs\Q VFBMS32 AI PCB"
sch_path = os.path.join(proj, "VFBMS32.kicad_sch")
dev_lib = r"C:\Program Files\KiCad\10.0\share\kicad\symbols\Device.kicad_sym"
ROOT = "a2322edc-ff52-449c-92df-24faffac0236"
SYM_UUIDS = {
    "C_FLT1": "6f1c2d4e-8a3b-4c5d-9e0f-1a2b3c4d5e01",
    "R_B33":  "6f1c2d4e-8a3b-4c5d-9e0f-1a2b3c4d5e02",
}

with open(sch_path, "r", encoding="utf-8", newline="") as f:
    sch = f.read()
nl = "\r\n" if "\r\n" in sch else "\n"

stamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
os.makedirs(os.path.join(proj, ".mcp-backups"), exist_ok=True)
shutil.copy2(sch_path, os.path.join(proj, ".mcp-backups", f"VFBMS32_{stamp}_pre_bottomrow.kicad_sch"))

def extract_block(text, start):
    depth = 0
    for i in range(start, len(text)):
        c = text[i]
        if c == "(":
            depth += 1
        elif c == ")":
            depth -= 1
            if depth == 0:
                return text[start:i + 1]
    raise ValueError("unbalanced")

# 1) ensure Device:C in lib_symbols
if '(symbol "Device:C"' not in sch:
    with open(dev_lib, "r", encoding="utf-8") as f:
        lib = f.read()
    idx = lib.find('(symbol "C"')
    blk = extract_block(lib, idx)
    blk = blk.replace('(symbol "C"', '(symbol "Device:C"', 1)
    blk = blk.replace("\n", nl)
    ls = sch.find("(lib_symbols")
    insert_at = sch.find(nl, ls) + len(nl)
    sch = sch[:insert_at] + "\t\t" + blk + nl + sch[insert_at:]
    print("Added Device:C to lib_symbols")

def sym(lib_id, ref, val, fp, x, y, uuid):
    return (
        f'\t(symbol (lib_id "{lib_id}"){nl}'
        f'\t\t(at {x} {y} 0){nl}'
        f'\t\t(unit 1){nl}'
        f'\t\t(exclude_from_sim no){nl}'
        f'\t\t(in_bom yes){nl}'
        f'\t\t(on_board yes){nl}'
        f'\t\t(dnp no){nl}'
        f'\t\t(uuid "{uuid}"){nl}'
        f'\t\t(property "Reference" "{ref}" (at {x} {y - 4} 0) (effects (font (size 1.27 1.27)))){nl}'
        f'\t\t(property "Value" "{val}" (at {x} {y + 4} 0) (effects (font (size 1.27 1.27)))){nl}'
        f'\t\t(property "Footprint" "{fp}" (at {x} {y} 0) (hide yes) (effects (font (size 1.27 1.27)))){nl}'
        f'\t\t(pin "1" (uuid "{uuid[:-2]}a1")){nl}'
        f'\t\t(pin "2" (uuid "{uuid[:-2]}a2")){nl}'
        f'\t\t(instances{nl}'
        f'\t\t\t(project "VFBMS32"{nl}'
        f'\t\t\t\t(path "/{ROOT}" (reference "{ref}") (unit 1)){nl}'
        f'\t\t\t){nl}'
        f'\t\t){nl}'
        f'\t){nl}'
    )

new_syms = ""
if '"C_FLT1"' not in sch:
    new_syms += sym("Device:C", "C_FLT1", "10uF_100V", "Capacitor_SMD:C_1812_4532Metric", 225.0, 105.0, SYM_UUIDS["C_FLT1"])
if '"R_B33"' not in sch:
    new_syms += sym("Device:R", "R_B33", "27R0", "Resistor_SMD:R_0805_2012Metric", 235.0, 105.0, SYM_UUIDS["R_B33"])

if new_syms:
    # insert before sheet_instances / final closing paren
    k = sch.find("\t(sheet_instances")
    if k == -1:
        k = sch.rstrip().rfind(")")
    sch = sch[:k] + new_syms + sch[k:]
    print("Added symbols")

with open(sch_path, "w", encoding="utf-8", newline="") as f:
    f.write(sch)
print("Saved", sch_path)
