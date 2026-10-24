import pcbnew

kicad_fp_dir = r"C:\Program Files\KiCad\10.0\share\kicad\footprints\Resistor_SMD.pretty"
fp1 = pcbnew.FootprintLoad(kicad_fp_dir, "R_0805_2012Metric")
fp2 = pcbnew.FootprintLoad(kicad_fp_dir, "R_0805_2012Metric")
print("Footprints loaded before LoadBoard:", type(fp1), type(fp2))

board = pcbnew.LoadBoard("qfbms32 ai pcb/qfbms32.kicad_pcb")
print("Board loaded after FootprintLoad:", type(board))
board.Add(fp1)
board.Add(fp2)
print("Both footprints added to board successfully!")
