"""Move C_F* to y=9.2 (above BQ bodies) to clear pad shorts."""
import pcbnew
from pathlib import Path

PCB = Path(__file__).resolve().parents[1] / "qfbms32.kicad_pcb"
board = pcbnew.LoadBoard(str(PCB))

for fp in board.GetFootprints():
    r = fp.GetReference()
    if r.startswith("C_F") and r[3:].isdigit():
        p = fp.GetPosition()
        fp.SetPosition(pcbnew.VECTOR2I(p.x, pcbnew.FromMM(9.2)))
        print(r, "y -> 9.2")

pcbnew.SaveBoard(str(PCB), board)
print("saved")
