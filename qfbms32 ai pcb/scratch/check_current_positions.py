import re

with open(r'c:\Users\quinn\Desktop\AI PCB CAD\Q VFBMS32 AI PCB\VFBMS32.kicad_pcb', 'r', encoding='utf-8') as f:
    text = f.read()

# Split by top-level footprints
# In KiCad 8/10, footprint starts with '\t(footprint "'
blocks = re.split(r'\n\t\(footprint\s+', text)
print(f"Total blocks found: {len(blocks)}")

targets = ['Q1', 'Q2', 'J_CHG1', 'J_BAT1', 'R_SH1', 'R_SH2', 'U_ESP1', 'J_USB1']

for b in blocks[1:]:
    # Find reference
    m_ref = re.search(r'\(property\s+\"Reference\"\s+\"([^\"]+)\"', b)
    if m_ref and m_ref.group(1) in targets:
        ref = m_ref.group(1)
        fp_name = b.split('"')[0]
        m_at = re.search(r'\(at\s+([\d.-]+)\s+([\d.-]+)(?:\s+([\d.-]+))?\)', b)
        at_str = f"at ({m_at.group(1)}, {m_at.group(2)}) rot {m_at.group(3) or '0'}" if m_at else "no at"
        models = re.findall(r'\(model\s+\"([^\"]+)\"', b)
        print(f"{ref} ({fp_name}): {at_str}, models={models}")
