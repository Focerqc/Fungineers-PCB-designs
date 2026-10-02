import subprocess
import re

cli = r"C:\Program Files\KiCad\10.0\bin\kicad-cli.exe"
diag_path = r"c:\Users\quinn\Desktop\AI PCB CAD\Q VFBMS32 AI PCB\scratch\diag.kicad_sch"

with open(r'c:\Users\quinn\Desktop\AI PCB CAD\Q VFBMS32 AI PCB\VFBMS32.kicad_sch', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Strip comments
clean_lines = [l for l in lines if not l.strip().startswith(';')]

# Let's check how many Q1, Q2, U_SSR1, R_G1, R_G2 exist
text = "".join(clean_lines)

# Notice lines 3663 to 3851 were duplicates in original
# Let's inspect where duplicate symbols are
dup_start = text.find('(symbol (lib_id "vfbms:AGM15T03LL")\n\t\t(at 195.0 45.0 0)\n\t\t(unit 1)\n\t\t(exclude_from_sim no)\n\t\t(in_bom yes)\n\t\t(on_board yes)\n\t\t(dnp no)\n\t\t(uuid "4e411f79-1647-498f-960d-57f84b99a27d")')
print("dup_start:", dup_start)

# If we remove the duplicate block:
if dup_start != -1:
    sheet_inst = text.rfind("(sheet_instances")
    text_dedup = text[:dup_start] + text[sheet_inst:]
    with open(diag_path, "w", encoding="utf-8") as f:
        f.write(text_dedup)
    res = subprocess.run([cli, "sch", "export", "pdf", diag_path, "-o", diag_path.replace(".kicad_sch", ".pdf")],
                         capture_output=True, text=True)
    print("Dedup + clean test:", res.returncode == 0, res.stderr.strip())
