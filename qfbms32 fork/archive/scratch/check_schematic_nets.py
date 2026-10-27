import os
import re

sch_path = r"c:\Users\quinn\Desktop\AI PCB CAD\Q VFBMS32 AI PCB\VFBMS32.kicad_sch"
if os.path.exists(sch_path):
    with open(sch_path, "r", encoding="utf-8") as f:
        text = f.read()
    
    labels = set(re.findall(r'\(label\s+\"([^\"]+)\"', text))
    glabels = set(re.findall(r'\(global_label\s+\"([^\"]+)\"', text))
    hlabels = set(re.findall(r'\(hierarchical_label\s+\"([^\"]+)\"', text))
    print(f"Labels found ({len(labels)}):", sorted(list(labels))[:30])
    print(f"Global labels found ({len(glabels)}):", sorted(list(glabels))[:30])
