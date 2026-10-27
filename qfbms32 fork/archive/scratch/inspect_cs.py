import re

with open("qfbms32 ai pcb/qfbms32.kicad_pcb", "r", encoding="utf-8", errors="ignore") as f:
    text = f.read()

lines = text.splitlines(keepends=True)
in_fp = False
curr_fp = []
for line in lines:
    if line.startswith('\t(footprint '):
        curr_fp = [line]
        in_fp = True
    elif in_fp:
        curr_fp.append(line)
        if line.startswith('\t)'):
            in_fp = False
            fp_text = "".join(curr_fp)
            if '"C_S1"' in fp_text or '"C_S2"' in fp_text:
                print(fp_text)
                print("="*60)
