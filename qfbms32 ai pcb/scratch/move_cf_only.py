"""Step 2: spread C_F1..C_F32; fix VC0 side nets. Fresh board load."""
import pcbnew
from pathlib import Path

PCB = Path(__file__).resolve().parents[1] / "qfbms32.kicad_pcb"
board = pcbnew.LoadBoard(str(PCB))

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


# Collect refs first (avoid iterator invalidation)
refs = []
for fp in board.GetFootprints():
    r = fp.GetReference()
    if r.startswith("C_F") and r[3:].isdigit():
        refs.append(r)
print("found", sorted(refs, key=lambda r: int(r[3:])))

n = 1
for bq, x0, y0 in (("BQ1", 78.0, 18.8), ("BQ2", 35.0, 18.8)):
    for vc in range(1, 17):
        ref = f"C_F{n}"
        fp = board.FindFootprintByReference(ref)
        if fp is None:
            print("missing", ref)
            n += 1
            continue
        if bq == "BQ1" and vc == 1:
            lo = "CELL0"
        elif bq == "BQ2" and vc == 1:
            lo = "CELL16"
        else:
            lo = f"{bq}_VC{vc-1}"
        hi = f"{bq}_VC{vc}"
        x = x0 + (vc - 1) * 1.8
        y = y0
        fp.SetPosition(pcbnew.VECTOR2I(pcbnew.FromMM(x), pcbnew.FromMM(y)))
        fp.SetOrientation(pcbnew.EDA_ANGLE(90, pcbnew.DEGREES_T))
        pads = sorted(list(fp.Pads()), key=lambda p: p.GetPosition().y)
        pads[0].SetNet(net(lo))
        pads[1].SetNet(net(hi))
        print(f"{ref} ({x:.1f},{y:.1f}) {lo}/{hi}")
        n += 1

pcbnew.SaveBoard(str(PCB), board)
print("saved")
