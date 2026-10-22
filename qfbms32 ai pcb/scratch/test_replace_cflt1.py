import os
import pcbnew

project_dir = r"c:\Users\quinn\Documents\GitHub\Fungineers PCB designs\Q VFBMS32 AI PCB"
pcb_path = os.path.join(project_dir, "VFBMS32.kicad_pcb")
kicad_fp_dir = r"C:\Program Files\KiCad\10.0\share\kicad\footprints"

board = pcbnew.LoadBoard(pcb_path)
fp = board.FindFootprintByReference("C_FLT1")
if fp:
    print("Found C_FLT1:")
    print("  Footprint:", fp.GetFPID().GetLibItemName())
    pos = fp.GetPosition()
    print(f"  Pos: ({pcbnew.ToMM(pos.x):.3f}, {pcbnew.ToMM(pos.y):.3f})")
    print(f"  Orientation: {fp.GetOrientation().AsDegrees()}")
else:
    print("C_FLT1 not found!")
