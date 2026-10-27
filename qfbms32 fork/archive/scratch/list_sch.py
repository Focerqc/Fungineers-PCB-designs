import re
import os

with open('qfbms32.kicad_sch', 'r', encoding='utf-8') as f:
    lines = f.readlines()

current_ref = ""
current_val = ""
current_fp = ""
for line in lines:
    m_ref = re.search(r'\(property "Reference" "([^"]+)"', line)
    if m_ref:
        current_ref = m_ref.group(1)
    m_val = re.search(r'\(property "Value" "([^"]+)"', line)
    if m_val:
        current_val = m_val.group(1)
    m_fp = re.search(r'\(property "Footprint" "([^"]*)"', line)
    if m_fp:
        current_fp = m_fp.group(1)
        if current_ref:
            print(f"{current_ref}: {current_val} | fp: {current_fp}")
            current_ref = ""
            current_val = ""
            current_fp = ""
