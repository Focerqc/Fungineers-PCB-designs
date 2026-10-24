sch_path = r"c:\Users\quinn\Documents\GitHub\Fungineers PCB designs\qfbms32 ai pcb\qfbms32.kicad_sch"
with open(sch_path, "r", encoding="utf-8") as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if any(k in line for k in ["Q1", "Q2", "U_SSR1", "R_G1", "R_G2", "R_CHG", "D_CHG", "474", "470k", "01X", "100k", "100R"]):
        start = max(0, i - 5)
        end = min(len(lines), i + 25)
        # print snippet
        print(f"--- Around line {i+1} ---")
        print("".join(lines[start:end]))
        print("="*40)
