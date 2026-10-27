import pcbnew
import os

project_dir = r"c:\Users\quinn\Documents\GitHub\Fungineers PCB designs\Q VFBMS32 AI PCB"
pcb_path = os.path.join(project_dir, "VFBMS32.kicad_pcb")
kicad_fp_dir = r"C:\Program Files\KiCad\10.0\share\kicad\footprints"

board = pcbnew.LoadBoard(pcb_path)
fp = board.FindFootprintByReference("C_FLT1")
print("Found C_FLT1:", fp is not None)

# Check 1812 dimensions
lib_path = os.path.join(kicad_fp_dir, "Capacitor_SMD.pretty")
new_fp = pcbnew.FootprintLoad(lib_path, "C_1812_4532Metric")
print("Loaded 1812:", new_fp is not None)

# Current position vs target:
target_x = 10.175
target_y = 16.625
print(f"Target pos: ({target_x}, {target_y})")

# Check bounding box / courtyard of 1812 at rotation 90
new_fp.SetPosition(pcbnew.VECTOR2I(pcbnew.FromMM(target_x), pcbnew.FromMM(target_y)))
new_fp.SetOrientation(pcbnew.EDA_ANGLE(90.0, pcbnew.DEGREES_T))
bbox = new_fp.GetBoundingBox()
print(f"1812 Bounding box: ({pcbnew.ToMM(bbox.GetX()):.2f}, {pcbnew.ToMM(bbox.GetY()):.2f}) W={pcbnew.ToMM(bbox.GetWidth()):.2f} H={pcbnew.ToMM(bbox.GetHeight()):.2f}")

# Check distances to D_CHG3 (x=6.90) and R_SH1 (x=14.00)
# 1812 width is along X when rotated 90 deg: width is ~3.2mm to 3.9mm
# Left edge of 1812: 10.18 - 3.9/2 = 8.23 mm
# Right edge of 1812: 10.18 + 3.9/2 = 12.13 mm
# Distance to D_CHG3 (x=6.90): 8.23 - 6.90 = 1.33 mm clearance!
# Distance to R_SH1 (x=14.00): 14.00 - 12.13 = 1.87 mm clearance!
# It fits perfectly!
