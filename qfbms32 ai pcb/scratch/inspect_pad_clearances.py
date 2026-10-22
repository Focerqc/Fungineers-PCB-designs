import os
import re

pcb_path = r"c:\Users\quinn\Documents\GitHub\Fungineers PCB designs\Q VFBMS32 AI PCB\VFBMS32.kicad_pcb"
with open(pcb_path, "r", encoding="utf-8") as f:
    text = f.read()

# Let's inspect J_CELL1 footprint definition and pads
m_cell1 = re.search(r'\(footprint [^\n]*\n[\s\S]*?\"Reference\" \"J_CELL1\"[\s\S]*?\n\t\)', text)
if m_cell1:
    print("=== J_CELL1 ===")
    print(m_cell1.group(0)[:1500])

# Let's inspect R_B1 footprint definition and pads
m_rb1 = re.search(r'\(footprint [^\n]*\n[\s\S]*?\"Reference\" \"R_B1\"[\s\S]*?\n\t\)', text)
if m_rb1:
    print("\n=== R_B1 ===")
    print(m_rb1.group(0)[:1500])

# Let's inspect R_F1 footprint definition and pads
m_rf1 = re.search(r'\(footprint [^\n]*\n[\s\S]*?\"Reference\" \"R_F1\"[\s\S]*?\n\t\)', text)
if m_rf1:
    print("\n=== R_F1 ===")
    print(m_rf1.group(0)[:1500])
