import os
import re

pcb_file = r"c:\Users\quinn\Desktop\AI PCB CAD\Q VFBMS32 AI PCB\VFBMS32.kicad_pcb"
sch_file = r"c:\Users\quinn\Desktop\AI PCB CAD\Q VFBMS32 AI PCB\VFBMS32.kicad_sch"

with open(pcb_file, "r", encoding="utf-8") as f:
    pcb_txt = f.read()

with open(sch_file, "r", encoding="utf-8") as f:
    sch_txt = f.read()

print("--- PCB FOOTPRINTS ---")
for m in re.finditer(r'\(footprint\s+"([^"]+)"[\s\S]*?\(property\s+"Reference"\s+"([^"]+)"[\s\S]*?\(property\s+"Value"\s+"([^"]+)"', pcb_txt):
    ref = m.group(2)
    val = m.group(3)
    fp = m.group(1)
    if any(k in ref for k in ["BOOST", "BUCK", "U4", "Q1", "Q2", "BAT", "CHG", "F1"]):
        print(f"PCB: {ref} = {val} [{fp}]")

print("\n--- ALL SCHEMATIC SYMBOLS ---")
for m in re.finditer(r'\(symbol[\s\S]*?\(property\s+"Reference"\s+"([^"]+)"[\s\S]*?\(property\s+"Value"\s+"([^"]+)"', sch_txt):
    ref = m.group(1)
    val = m.group(2)
    if ref.startswith("U") or "BOOST" in ref or "BUCK" in ref or "SPV" in val or "TPS" in val:
        print(f"SCH: {ref} = {val}")


