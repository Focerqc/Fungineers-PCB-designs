with open('VFBMS32.kicad_sch', 'r', encoding='utf-8') as f:
    text = f.read()

import re
tags = set(re.findall(r'^\t*\(([a-z_]+)', text, re.MULTILINE))
print("Top-level / block tags:", sorted(tags))
