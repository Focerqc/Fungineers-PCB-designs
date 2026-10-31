"""Fix VBOOST short to VBAT_S and re-place C_F* with non-shorting pitch."""
from __future__ import annotations

from pathlib import Path

import pcbnew

PCB = Path(__file__).resolve().parents[1] / "qfbms32.kicad_pcb"
FP_CAP = Path(r"C:\Program Files\KiCad\10.0\share\kicad\footprints\Capacitor_SMD.pretty")

board = pcbnew.LoadBoard(str(PCB))


def net(name: str):
    n = board.FindNet(name)
    if n and n.GetNetCode() > 0:
        return n
    ni = pcbnew.NETINFO_ITEM(board, name)
    board.Add(ni)
    return ni


# Remove existing VBOOST/GND tracks we added (all tracks currently are ours)
to_remove = list(board.GetTracks())
for t in to_remove:
    board.Remove(t)
print("removed tracks", len(to_remove))

# C_SSR1 @ (28.45,1.75) rot90: pad1 y=2.525 VBOOST, pad2 y=0.975 GND
# C_SSR2 @ (30.00,1.70) rot90: pad1 y=2.65 VBOOST, pad2 y=0.75 GND
# U_SSR1 pad5 VBOOST (31.925,1.595), pad6 CELL32 (31.925,2.865), pad4 GND (41.475,1.595)
# Route VBOOST along y=1.40 (between pad5 and pad6) then down to pad5 only.

def add_track(x1, y1, x2, y2, netname, width=0.25):
    t = pcbnew.PCB_TRACK(board)
    t.SetStart(pcbnew.VECTOR2I(pcbnew.FromMM(x1), pcbnew.FromMM(y1)))
    t.SetEnd(pcbnew.VECTOR2I(pcbnew.FromMM(x2), pcbnew.FromMM(y2)))
    t.SetWidth(pcbnew.FromMM(width))
    t.SetLayer(pcbnew.F_Cu)
    t.SetNet(net(netname))
    board.Add(t)


# VBOOST: caps pad1 → join at (30, 2.0) → go to x=31.925 at y=1.40 → pad5
add_track(28.45, 2.525, 30.00, 2.525, "VBOOST", 0.25)
add_track(30.00, 2.525, 30.00, 2.65, "VBOOST", 0.25)
add_track(30.00, 2.65, 30.00, 1.40, "VBOOST", 0.25)
add_track(30.00, 1.40, 31.925, 1.40, "VBOOST", 0.25)
add_track(31.925, 1.40, 31.925, 1.595, "VBOOST", 0.25)

# GND along top edge y=0.55, clear of pads, to pad4
add_track(28.45, 0.975, 28.45, 0.55, "GND", 0.25)
add_track(30.00, 0.75, 30.00, 0.55, "GND", 0.25)
add_track(28.45, 0.55, 41.475, 0.55, "GND", 0.3)
add_track(41.475, 0.55, 41.475, 1.595, "GND", 0.3)

# Remove old C_F*
removed = 0
for fp in list(board.GetFootprints()):
    if fp.GetReference().startswith("C_F"):
        board.Remove(fp)
        removed += 1
print("removed C_F", removed)


def place_cf(ref, x, y, net_a, net_b, rot=90):
    fp = pcbnew.FootprintLoad(str(FP_CAP), "C_0402_1005Metric")
    board.Add(fp)
    fp.SetReference(ref)
    fp.SetValue("0.22uF")
    fp.SetPosition(pcbnew.VECTOR2I(pcbnew.FromMM(x), pcbnew.FromMM(y)))
    fp.SetOrientation(pcbnew.EDA_ANGLE(rot, pcbnew.DEGREES_T))
    fp.Reference().SetVisible(False)
    fp.Value().SetVisible(False)
    pads = sorted(fp.Pads(), key=lambda p: p.GetPosition().y)
    # after 90° rot, pads stacked in Y — lower Y = net_b, higher Y = net_a
    pads[0].SetNet(net(net_b))
    pads[1].SetNet(net(net_a))


# Pitch 1.8 mm in X; vertical 0402 body ~1.0 mm wide → courtyard OK
# BQ1 cluster near x=80.. , BQ2 near x=37..
n = 1
for bq, x0, y0 in (("BQ1", 78.0, 18.8), ("BQ2", 35.0, 18.8)):
    for vc in range(1, 17):
        lo = "CELL0" if (bq == "BQ1" and vc == 1) else (
            "CELL16" if (bq == "BQ2" and vc == 1) else f"{bq}_VC{vc-1}"
        )
        hi = f"{bq}_VC{vc}"
        place_cf(f"C_F{n}", x0 + (vc - 1) * 1.8, y0, hi, lo, rot=90)
        n += 1

pcbnew.SaveBoard(str(PCB), board)
print("saved; tracks", sum(1 for _ in board.GetTracks()))
