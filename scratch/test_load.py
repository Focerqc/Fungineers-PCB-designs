import os
import pcbnew

kicad_fp_dir = r"C:\Program Files\KiCad\10.0\share\kicad\footprints"
diode_lib = os.path.join(kicad_fp_dir, "Diode_SMD.pretty")
res_lib = os.path.join(kicad_fp_dir, "Resistor_SMD.pretty")

fp_diode = pcbnew.FootprintLoad(diode_lib, "D_SOD-123F")
print("FootprintLoad D_SOD-123F:", fp_diode is not None)

fp_res = pcbnew.FootprintLoad(res_lib, "R_0603_1608Metric")
print("FootprintLoad R_0603_1608Metric:", fp_res is not None)
