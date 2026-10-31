"""Park C_F* between JST row and R_B row (y~26.3), under matching cell X bands."""
import pcbnew
from pathlib import Path

PCB = Path(__file__).resolve().parents[1] / "qfbms32.kicad_pcb"
board = pcbnew.LoadBoard(str(PCB))

# C_F1..16 BQ1 (lower cells, right): under J_CELL1/2 band
for i in range(1, 17):
    fp = board.FindFootprintByReference(f"C_F{i}")
    x = 70.0 + (i - 1) * 1.9
    y = 26.3
    fp.SetPosition(pcbnew.VECTOR2I(pcbnew.FromMM(x), pcbnew.FromMM(y)))
    if fp.IsFlipped():
        pass
    print(f"C_F{i} -> ({x:.1f},{y:.1f})")

# C_F17..32 BQ2 (upper cells, left)
for i in range(17, 33):
    fp = board.FindFootprintByReference(f"C_F{i}")
    x = 36.0 + (i - 17) * 1.9
    y = 26.3
    fp.SetPosition(pcbnew.VECTOR2I(pcbnew.FromMM(x), pcbnew.FromMM(y)))
    print(f"C_F{i} -> ({x:.1f},{y:.1f})")

pcbnew.SaveBoard(str(PCB), board)
print("saved")
