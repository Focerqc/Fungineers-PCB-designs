import os
import re

fw_dir = r"c:\Users\quinn\Desktop\AI PCB CAD\Q VFBMS32 AI PCB\_reference\firmware"
with open(os.path.join(fw_dir, "hw.c"), "r", encoding="utf-8") as f:
    text = f.read()

# Search for BQ subcommands and register writes
for line in text.splitlines():
    if any(k in line for k in ["FET", "CFET", "DFET", "CHG_EN", "PCHG_EN", "PSW_EN", "OUT_EN", "ManufacturingStatus"]):
        print(line)
