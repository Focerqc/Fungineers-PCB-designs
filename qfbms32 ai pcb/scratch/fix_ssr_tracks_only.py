"""Step 1: rewrite SSR VBOOST/GND tracks only, then save."""
import pcbnew
from pathlib import Path

PCB = Path(__file__).resolve().parents[1] / "qfbms32.kicad_pcb"
board = pcbnew.LoadBoard(str(PCB))

# Build net lookup from pads that already have nets
net_cache = {}
for fp in board.GetFootprints():
    for pad in fp.Pads():
        if pad.GetNetCode() > 0:
            net_cache[pad.GetNetname()] = pad.GetNet()


def net(name):
    if name in net_cache:
        return net_cache[name]
    ni = pcbnew.NETINFO_ITEM(board, name)
    board.Add(ni)
    net_cache[name] = ni
    return ni


for t in list(board.GetTracks()):
    board.Remove(t)


def add_track(x1, y1, x2, y2, netname, width=0.25):
    t = pcbnew.PCB_TRACK(board)
    t.SetStart(pcbnew.VECTOR2I(pcbnew.FromMM(x1), pcbnew.FromMM(y1)))
    t.SetEnd(pcbnew.VECTOR2I(pcbnew.FromMM(x2), pcbnew.FromMM(y2)))
    t.SetWidth(pcbnew.FromMM(width))
    t.SetLayer(pcbnew.F_Cu)
    t.SetNet(net(netname))
    board.Add(t)


add_track(28.45, 2.525, 30.00, 2.525, "VBOOST", 0.25)
add_track(30.00, 2.525, 30.00, 2.65, "VBOOST", 0.25)
add_track(30.00, 2.65, 30.00, 1.40, "VBOOST", 0.25)
add_track(30.00, 1.40, 31.925, 1.40, "VBOOST", 0.25)
add_track(31.925, 1.40, 31.925, 1.595, "VBOOST", 0.25)

add_track(28.45, 0.975, 28.45, 0.55, "GND", 0.25)
add_track(30.00, 0.75, 30.00, 0.55, "GND", 0.25)
add_track(28.45, 0.55, 41.475, 0.55, "GND", 0.3)
add_track(41.475, 0.55, 41.475, 1.595, "GND", 0.3)

pcbnew.SaveBoard(str(PCB), board)
print("tracks saved", sum(1 for _ in board.GetTracks()))
