import re
from pathlib import Path

t = Path(r"c:\Users\quinn\Documents\GitHub\Fungineers PCB designs\qfbms32 ai pcb\scratch\pinouts\agm_pinout.html").read_text(encoding="utf-8", errors="ignore")
for m in re.finditer(r".{80}pdf.{80}", t, re.I):
    s = m.group(0).replace("\n", " ")
    if "ISO" in s or "PCI" in s or "Certificate" in s:
        continue
    print(s)
    print("---")
