import os
import pcbnew

kicad_fp_dir = r"C:\Program Files\KiCad\10.0\share\kicad\footprints"
lib_path = os.path.join(kicad_fp_dir, "Capacitor_SMD.pretty")
fp = pcbnew.FootprintLoad(lib_path, "C_1812_4532Metric")
print("Loaded footprint:", fp.GetFPID().GetLibItemName() if fp else "FAILED")
