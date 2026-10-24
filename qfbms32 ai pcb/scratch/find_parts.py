import re

with open("qfbms32 ai pcb/qfbms32.kicad_pcb", "r", encoding="utf-8", errors="ignore") as f:
    lines = f.readlines()

in_fp = False
fp_lines = []
all_fps = []

for line in lines:
    if line.startswith('\t(footprint '):
        if fp_lines:
            all_fps.append("".join(fp_lines))
        fp_lines = [line]
        in_fp = True
    elif in_fp:
        if line.startswith('\t)'):
            fp_lines.append(line)
            all_fps.append("".join(fp_lines))
            fp_lines = []
            in_fp = False
        else:
            fp_lines.append(line)

print(f"Total footprints parsed: {len(all_fps)}")

for fp_str in all_fps:
    # fp name
    m_name = re.search(r'\(footprint\s+"([^"]+)"', fp_str)
    name = m_name.group(1) if m_name else ""
    m_at = re.search(r'\(at\s+([-\d\.]+)\s+([-\d\.]+)(?:\s+([-\d\.]+))?\)', fp_str)
    m_ref = re.search(r'\(property\s+"Reference"\s+"([^"]+)"', fp_str)
    m_val = re.search(r'\(property\s+"Value"\s+"([^"]+)"', fp_str)
    
    if m_at and m_ref:
        x, y = float(m_at.group(1)), float(m_at.group(2))
        rot = float(m_at.group(3)) if m_at.group(3) else 0.0
        ref = m_ref.group(1)
        val = m_val.group(1) if m_val else ""
        if 15.0 <= x <= 20.0 and 13.0 <= y <= 19.0:
            print(f"[NEAR BOX] Ref: {ref:10} Val: {val:15} FP: {name:25} Pos: ({x:6.2f}, {y:6.2f}, {rot:3.0f})")
        if "S1" in ref or "S2" in ref or "CS1" in ref or "CS2" in ref:
            print(f"[MATCH REF] Ref: {ref:10} Val: {val:15} FP: {name:25} Pos: ({x:6.2f}, {y:6.2f}, {rot:3.0f})")
