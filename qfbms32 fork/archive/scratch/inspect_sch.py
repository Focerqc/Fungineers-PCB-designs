import re

with open('qfbms32.kicad_sch', 'r', encoding='utf-8') as f:
    sch = f.read()

sheets = re.findall(r'\(sheet\b.*?\)', sch, re.DOTALL)
print('Hierarchical sheets count:', len(sheets))
for s in sheets:
    print(s[:200])

labels = re.findall(r'\((?:hierarchical_)?label\s+"([^"]+)"', sch)
print('Unique labels:', len(set(labels)))
