"""Put C_F* on back copper under BQ areas — clears JST/R_B front shorts."""
import pcbnew
from pathlib import Path

PCB = Path(__file__).resolve().parents[1] / "qfbms32.kicad_pcb"
board = pcbnew.LoadBoard(str(PCB))

# Place under BQ footprints on back: BQ1 ~88, BQ2 ~45
for i in range(1, 17):
    fp = board.FindFootprintByReference(f"C_F{i}")
    if not fp.IsFlipped():
        fp.Flip(fp.GetPosition(), False)
    row = 0 if i <= 8 else 1
    col = (i - 1) % 8
    x = 80.0 + col * 1.9
    y = 11.0 + row * 2.2
    fp.SetPosition(pcbnew.VECTOR2I(pcbnew.FromMM(x), pcbnew.FromMM(y)))
    print(f"C_F{i} B.Cu ({x:.1f},{y:.1f}) flipped={fp.IsFlipped()}")

for i in range(17, 33):
    fp = board.FindFootprintByReference(f"C_F{i}")
    if not fp.IsFlipped():
        fp.Flip(fp.GetPosition(), False)
    j = i - 17
    row = 0 if j < 8 else 1
    col = j % 8
    x = 37.0 + col * 1.9
    y = 11.0 + row * 2.2
    fp.SetPosition(pcbnew.VECTOR2I(pcbnew.FromMM(x), pcbnew.FromMM(y)))
    print(f"C_F{i} B.Cu ({x:.1f},{y:.1f}) flipped={fp.IsFlipped()}")

pcbnew.SaveBoard(str(PCB), board)
print("saved")
