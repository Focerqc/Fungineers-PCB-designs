with open('Q VFBMS32 AI PCB/VFBMS32.kicad_pcb', 'r', encoding='utf-8') as f:
    text = f.read()

for ref in ['D_V1', 'D_V2', 'D_V3', 'C_FLT1', 'R_SH1']:
    idx = text.find(f'"{ref}"')
    if idx != -1:
        # find start of footprint
        fp_start = text.rfind('(footprint', 0, idx)
        fp_end = text.find('\n\t)', idx)
        print(f"=== {ref} ===")
        print(text[fp_start:fp_start+300])
