import re

with open('qfbms32.kicad_sch', 'r', encoding='utf-8') as f:
    sch = f.read()

# find Q1 symbol in sch
idx = sch.find('(property "Reference" "Q1"')
if idx != -1:
    print(sch[idx-200:idx+1500])
