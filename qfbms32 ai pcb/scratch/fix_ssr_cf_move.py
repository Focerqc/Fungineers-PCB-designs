"""Rewrite SSR tracks clear of pad6; spread existing C_F* to 1.8mm pitch."""
import pcbnew
from pathlib import Path

PCB = Path(__file__).resolve().parents[1] / "qfbms32.kicad_pcb"
board = pcbnew.LoadBoard(str(PCB))
nets_by_name = board.GetNetInfo().NetsByName()


def net(name: str):
    # NetsByName map: UTF8 keys
    if name in nets_by_name:
        return nets_by_name[name]
    ni = pcbnew.NETINFO_ITEM(board, name)
    board.Add(ni)
    nets_by_name[name] = ni
    return ni


# Clear all tracks (only SSR stubs exist)
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


def assign_cf(ref, x, y, net_a, net_b):
    fp = board.FindFootprintByReference(ref)
    if not fp:
        print("missing", ref)
        return
    fp.SetPosition(pcbnew.VECTOR2I(pcbnew.FromMM(x), pcbnew.FromMM(y)))
    fp.SetOrientation(pcbnew.EDA_ANGLE(90, pcbnew.DEGREES_T))
    fp.SetValue("0.22uF")
    pads = sorted(fp.Pads(), key=lambda p: p.GetPosition().y)
    pads[0].SetNet(net(net_b))
    pads[1].SetNet(net(net_a))
    print(f"{ref} -> ({x:.1f},{y:.1f}) {net_b}/{net_a}")


n = 1
for bq, x0, y0 in (("BQ1", 78.0, 18.8), ("BQ2", 35.0, 18.8)):
    for vc in range(1, 17):
        if bq == "BQ1" and vc == 1:
            lo = "CELL0"
        elif bq == "BQ2" and vc == 1:
            lo = "CELL16"
        else:
            lo = f"{bq}_VC{vc-1}"
        hi = f"{bq}_VC{vc}"
        assign_cf(f"C_F{n}", x0 + (vc - 1) * 1.8, y0, hi, lo)
        n += 1

pcbnew.SaveBoard(str(PCB), board)
print("saved OK, tracks", sum(1 for _ in board.GetTracks()))
