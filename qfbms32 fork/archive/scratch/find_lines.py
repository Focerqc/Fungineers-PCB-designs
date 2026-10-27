with open("qfbms32 ai pcb/qfbms32.kicad_pcb", "r", encoding="utf-8") as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if '"C_S1"' in line or '"C_S2"' in line:
        print(f"Line {i+1}: {line.strip()}")
