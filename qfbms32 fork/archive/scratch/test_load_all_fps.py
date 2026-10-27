import os
import pcbnew

kicad_fp_dir = r"C:\Program Files\KiCad\10.0\share\kicad\footprints"
custom_fp_dir = r"c:\Users\quinn\Desktop\AI PCB CAD\Q VFBMS32 AI PCB\vfbms.pretty"

test_fps = [
    (custom_fp_dir, "", "XT30PW-F_Lugs"),
    (custom_fp_dir, "", "XT30PW-M_Lugs"),
    (custom_fp_dir, "", "TOLL-8_AGM15T03LL"),
    (custom_fp_dir, "", "ESP32-C3-MINI-1"),
    (custom_fp_dir, "", "USB_C_Receptacle_16P"),
    (kicad_fp_dir, "Package_QFP.pretty", "TQFP-48-1EP_7x7mm_P0.5mm_EP5x5mm_ThermalVias"),
    (kicad_fp_dir, "Package_SO.pretty", "TSSOP-8_4.4x3mm_P0.65mm"),
    (kicad_fp_dir, "Package_SO.pretty", "SOIC-8_3.9x4.9mm_P1.27mm"),
    (kicad_fp_dir, "Package_DFN_QFN.pretty", "Texas_RTE_WQFN-16-1EP_3x3mm_P0.5mm_EP1.2x0.8mm_ThermalVias"),
    (kicad_fp_dir, "Inductor_SMD.pretty", "L_7.3x7.3_H4.5"),
    (kicad_fp_dir, "Inductor_SMD.pretty", "L_6.3x6.3_H3"),
    (kicad_fp_dir, "Capacitor_Tantalum_SMD.pretty", "CP_EIA-6032-28_Kemet-C"),
    (kicad_fp_dir, "Connector_JST.pretty", "JST_GH_BM04B-GHS-TBT_1x04-1MP_P1.25mm_Vertical"),
    (kicad_fp_dir, "Connector_JST.pretty", "JST_GH_BM06B-GHS-TBT_1x06-1MP_P1.25mm_Vertical"),
    (kicad_fp_dir, "Connector_JST.pretty", "JST_GH_BM08B-GHS-TBT_1x08-1MP_P1.25mm_Vertical"),
    (kicad_fp_dir, "Connector_JST.pretty", "JST_GH_BM09B-GHS-TBT_1x09-1MP_P1.25mm_Vertical"),
    (kicad_fp_dir, "Connector_JST.pretty", "JST_GH_BM10B-GHS-TBT_1x10-1MP_P1.25mm_Vertical"),
    (kicad_fp_dir, "Connector_JST.pretty", "JST_GH_BM02B-GHS-TBT_1x02-1MP_P1.25mm_Vertical"),
    (kicad_fp_dir, "Resistor_SMD.pretty", "R_2512_6332Metric"),
    (kicad_fp_dir, "Resistor_SMD.pretty", "R_1206_3216Metric"),
    (kicad_fp_dir, "Resistor_SMD.pretty", "R_0805_2012Metric"),
    (kicad_fp_dir, "Resistor_SMD.pretty", "R_0603_1608Metric"),
    (kicad_fp_dir, "Resistor_SMD.pretty", "R_0402_1005Metric"),
    (kicad_fp_dir, "Capacitor_SMD.pretty", "C_1206_3216Metric"),
    (kicad_fp_dir, "Capacitor_SMD.pretty", "C_0805_2012Metric"),
    (kicad_fp_dir, "Capacitor_SMD.pretty", "C_0603_1608Metric"),
    (kicad_fp_dir, "Capacitor_SMD.pretty", "C_0402_1005Metric"),
    (kicad_fp_dir, "Diode_SMD.pretty", "D_SOD-323"),
    (kicad_fp_dir, "Diode_SMD.pretty", "D_SOD-123"),
    (kicad_fp_dir, "Fuse.pretty", "Fuse_2512_6332Metric"),
]

all_ok = True
for base, lib, name in test_fps:
    p = os.path.join(base, lib) if lib else base
    fp = pcbnew.FootprintLoad(p, name)
    if not fp:
        print(f"FAILED to load {lib}/{name}")
        all_ok = False
if all_ok:
    print("ALL footprints loaded successfully!")
