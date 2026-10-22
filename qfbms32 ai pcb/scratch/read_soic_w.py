import os

soic_w_path = r'C:\Program Files\KiCad\10.0\share\kicad\footprints\Package_SO.pretty\SOIC-8_7.5x5.85mm_P1.27mm.kicad_mod'
with open(soic_w_path, 'r', encoding='utf-8') as f:
    print("=== SOIC-8_7.5x5.85mm_P1.27mm ===")
    print(f.read()[:1000])

sop_w_path = r'C:\Program Files\KiCad\10.0\share\kicad\footprints\Package_SO.pretty\SOP-8_6.62x9.15mm_P2.54mm.kicad_mod'
if os.path.exists(sop_w_path):
    with open(sop_w_path, 'r', encoding='utf-8') as f:
        print("=== SOP-8_6.62x9.15mm_P2.54mm ===")
        print(f.read()[:1000])
