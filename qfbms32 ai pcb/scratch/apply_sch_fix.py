import os
import shutil

sch_path = r"c:\Users\quinn\Desktop\AI PCB CAD\Q VFBMS32 AI PCB\VFBMS32.kicad_sch"
bak_path = r"c:\Users\quinn\Desktop\AI PCB CAD\Q VFBMS32 AI PCB\scratch\VFBMS32.kicad_sch.bak"

shutil.copy2(sch_path, bak_path)

with open(sch_path, "r", encoding="utf-8") as f:
    lines = f.readlines()

clean_lines = [l for l in lines if not l.strip().startswith(';')]
text = "".join(clean_lines)

dup_start = text.find('(symbol (lib_id "vfbms:AGM15T03LL")\n\t\t(at 195.0 45.0 0)\n\t\t(unit 1)\n\t\t(exclude_from_sim no)\n\t\t(in_bom yes)\n\t\t(on_board yes)\n\t\t(dnp no)\n\t\t(uuid "4e411f79-1647-498f-960d-57f84b99a27d")')
if dup_start != -1:
    sheet_inst = text.rfind("(sheet_instances")
    text = text[:dup_start] + text[sheet_inst:]

with open(sch_path, "w", encoding="utf-8") as f:
    f.write(text)

print("Saved cleaned VFBMS32.kicad_sch")
