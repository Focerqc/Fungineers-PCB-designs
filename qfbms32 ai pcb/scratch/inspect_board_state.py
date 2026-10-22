import os
import pcbnew

project_dir = r"c:\Users\quinn\Desktop\AI PCB CAD\Q VFBMS32 AI PCB"
pcb_path = os.path.join(project_dir, "VFBMS32.kicad_pcb")

board = pcbnew.LoadBoard(pcb_path)
print("Board loaded successfully")
print("Number of footprints:", len(board.GetFootprints()))
print("Number of tracks/vias:", len(board.GetTracks()))
print("Number of zones:", len(board.Zones()))

# List nets
netinfo = board.GetNetInfo()
nets = [netinfo.GetNetItem(i).GetNetname() for i in range(netinfo.GetNetCount())]
print(f"Total nets ({len(nets)}):", nets[:20])

# Inspect key power footprints
for fp in board.GetFootprints():
    ref = fp.GetReference()
    if ref in ["Q1", "Q2", "R_SH1", "R_SH2", "J_BAT1", "J_CHG1", "U_SSR1", "U7", "U_ESP1"]:
        pos = fp.GetPosition()
        rot = fp.GetOrientation().AsDegrees()
        print(f"{ref} ({fp.GetValue()}): at ({pos.x/1e6:.2f}, {pos.y/1e6:.2f}) rot {rot:.1f}")
