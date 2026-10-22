import os
import subprocess
import re

cli = r"C:\Program Files\KiCad\10.0\bin\kicad-cli.exe"
sch_path = r"c:\Users\quinn\Desktop\AI PCB CAD\Q VFBMS32 AI PCB\VFBMS32.kicad_sch"
diag_path = r"c:\Users\quinn\Desktop\AI PCB CAD\Q VFBMS32 AI PCB\scratch\diag.kicad_sch"

with open(sch_path, "r", encoding="utf-8") as f:
    text = f.read()

def test_sch(content):
    with open(diag_path, "w", encoding="utf-8") as f:
        f.write(content)
    res = subprocess.run([cli, "sch", "export", "pdf", diag_path, "-o", diag_path.replace(".kicad_sch", ".pdf")],
                         capture_output=True, text=True)
    return res.returncode == 0, res.stderr.strip()

tail = "\n\t(sheet_instances\n\t\t(path \"/\"\n\t\t\t(page \"1\")\n\t\t)\n\t)\n)\n"

m = re.search(r'\(symbol\s*\(lib_id\s*"Interface_CAN_LIN:SN65HVD230"\)[\s\S]*?\n\t\)', text)
u5_end = m.end()

base = text[:u5_end]

# Extract all top-level elements after U5
# In the schematic, after U5 there are labels and symbols.
after_u5 = text[u5_end:text.rfind("(sheet_instances")]

# Let's split after_u5 into individual s-expressions
# An s-expression starts with \n\t( and ends when parens balance
elements = []
depth = 0
cur = []
in_str = False
escape = False

i = 0
while i < len(after_u5):
    c = after_u5[i]
    if c == '"' and not escape:
        in_str = not in_str
    elif c == '\\' and in_str:
        escape = not escape
        cur.append(c)
        i += 1
        continue
    else:
        escape = False

    if not in_str:
        if c == '(':
            depth += 1
        elif c == ')':
            depth -= 1
            if depth == 0 and cur:
                cur.append(c)
                elem_str = "".join(cur).strip()
                if elem_str:
                    elements.append(elem_str)
                cur = []
                i += 1
                continue
    if depth > 0 or c == '(':
        cur.append(c)
    i += 1

print(f"Total elements after U5: {len(elements)}")

# Test adding elements one by one
acc = base
for idx, el in enumerate(elements):
    first_line = el.split('\n')[0][:60]
    candidate = acc + "\n\t" + el + tail
    ok, err = test_sch(candidate)
    if not ok:
        print(f"FAILED on element {idx}: {first_line}")
        print("Error:", err)
        print("Full element:")
        print(el)
        break
    else:
        print(f"Element {idx} OK: {first_line}")
        acc = acc + "\n\t" + el
