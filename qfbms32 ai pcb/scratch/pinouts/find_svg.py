import re
from pathlib import Path

t = Path(r"c:\Users\quinn\Documents\GitHub\Fungineers PCB designs\qfbms32 ai pcb\scratch\pinouts\agm_pinout.html").read_text(encoding="utf-8", errors="ignore")
for m in re.finditer(r"https:[^\"']+8ef78bec[^\"']+", t):
    print("PDF", m.group(0)[:400])
for m in re.finditer(r"[^\"']+af191cd1[^\"']+", t):
    print("SVG", m.group(0)[:400])
    print("---")
