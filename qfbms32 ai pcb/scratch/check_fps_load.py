import pcbnew
import os

project_dir = r"c:\Users\quinn\Desktop\AI PCB CAD\Q VFBMS32 AI PCB"
kicad_fp_dir = r"C:\Program Files\KiCad\10.0\share\kicad\footprints"
custom_fp_dir = os.path.join(project_dir, "vfbms.pretty")

test_fps = [
    (kicad_fp_dir, "Fuse.pretty", "Fuse_2410_6125Metric"),
    (kicad_fp_dir, "Package_SO.pretty", "SOIC-16_3.9x9.9mm_P1.27mm"),
    (kicad_fp_dir, "Package_SO.pretty", "SOIC-8_3.9x4.9mm_P1.27mm"),
    (kicad_fp_dir, "Inductor_SMD.pretty", "L_7.3x7.3_H4.5"),
    (kicad_fp_dir, "Capacitor_Tantalum_SMD.pretty", "CP_EIA-6032-28_Kemet-C"),
    (custom_fp_dir, "", "ESP32-C3-MINI-1"),
    (custom_fp_dir, "", "USB_C_Receptacle_16P"),
    (custom_fp_dir, "", "TOLL-8_AGM15T03LL"),
    (custom_fp_dir, "", "XT30PW-F_Lugs"),
    (custom_fp_dir, "", "XT30PW-M_Lugs"),
]

for base, lib, name in test_fps:
    p = os.path.join(base, lib) if lib else base
    fp = pcbnew.FootprintLoad(p, name)
    print(f"{name:30s}: {'OK' if fp else 'FAILED'}")
