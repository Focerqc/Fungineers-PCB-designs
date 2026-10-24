import re

with open('qfbms32.kicad_sch', 'r', encoding='utf-8') as f:
    sch = f.read()

idx = sch.find('(symbol "qfbms:H2440_SSR"')
if idx != -1:
    print(sch[idx:idx+2000])
