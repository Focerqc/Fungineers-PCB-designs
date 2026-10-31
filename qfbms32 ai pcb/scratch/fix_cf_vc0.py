"""Tie differential caps on VC0 side to CELL0 / CELL16 (BQ VC0 pins)."""
import pcbnew
from pathlib import Path

PCB = Path(__file__).resolve().parents[1] / "qfbms32.kicad_pcb"
board = pcbnew.LoadBoard(str(PCB))


def net(name):
    n = board.FindNet(name)
    if n and n.GetNetCode() > 0:
        return n
    ni = pcbnew.NETINFO_ITEM(board, name)
    board.Add(ni)
    return ni


# C_F1 is BQ1_VC1 -- BQ1_VC0; retarget BQ1_VC0 pad to CELL0
# C_F17 is BQ2_VC1 -- BQ2_VC0; retarget to CELL16
for ref, want in (("C_F1", "CELL0"), ("C_F17", "CELL16")):
    fp = board.FindFootprintByReference(ref)
    for p in fp.Pads():
        if "VC0" in (p.GetNetname() or ""):
            p.SetNet(net(want))
            print(ref, "pad", p.GetNumber(), "->", want)

pcbnew.SaveBoard(str(PCB), board)
print("fixed")
