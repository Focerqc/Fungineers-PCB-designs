import pcbnew

kicad_fp_dir = r"C:\Program Files\KiCad\10.0\share\kicad\footprints\Resistor_SMD.pretty"
fp1 = pcbnew.FootprintLoad(kicad_fp_dir, "R_0805_2012Metric")
print("First call:", type(fp1))
try:
    fp2 = pcbnew.FootprintLoad(kicad_fp_dir, "R_0805_2012Metric")
    print("Second call:", type(fp2))
except Exception as e:
    print("Second call error:", e)
