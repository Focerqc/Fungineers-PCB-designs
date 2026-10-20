import os
import pcbnew

pcb_path = r"c:\Users\quinn\Documents\GitHub\Fungineers PCB designs\Q VFBMS32 AI PCB\VFBMS32.kicad_pcb"
board = pcbnew.LoadBoard(pcb_path)

print(f"Board loaded successfully! Total footprints: {len(list(board.GetFootprints()))}")

# Check D_V1, D_V2, D_V3
for ref in ['D_V1', 'D_V2', 'D_V3']:
    fp = board.FindFootprintByReference(ref)
    if fp:
        pos = fp.GetPosition()
        print(f"Found {ref}: pos=({pcbnew.ToMM(pos.x)}, {pcbnew.ToMM(pos.y)}) mm, libItem={fp.GetFPID().GetLibItemName()}")
    else:
        print(f"Did not find {ref}")
