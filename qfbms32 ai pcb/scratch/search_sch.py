import os, re

with open('qfbms32.kicad_sch', 'r', encoding='utf-8') as f:
    sch = f.read()

# Let's search for U_SSR1, R_SSR1, Q1
for name in ['U_SSR1', 'R_SSR1', 'R_G1', 'R_GS1']:
    idx = sch.find(name)
    if idx != -1:
        start = max(0, idx - 500)
        end = min(len(sch), idx + 2000)
        print(f"=== {name} in schematic ===")
        print(sch[start:end])
        print("="*60)
