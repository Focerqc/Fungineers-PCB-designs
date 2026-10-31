"""
Park netless R_B* clear of the cell-filter corridor, then route
J_CELL -> R_F CELL stubs on F.Cu only.
"""
from __future__ import annotations

import shutil
from pathlib import Path

import pcbnew

ROOT = Path(__file__).resolve().parents[1]
PCB = ROOT / "qfbms32.kicad_pcb"
HIST = ROOT / ".history"


def net(board, name):
    existing = board.FindNet(name)
    if existing and existing.GetNetCode() > 0:
        return existing
    ni = pcbnew.NETINFO_ITEM(board, name)
    board.Add(ni)
    return ni


def add_track(board, x1, y1, x2, y2, netname, width=0.2):
    if abs(x1 - x2) < 1e-4 and abs(y1 - y2) < 1e-4:
        return
    t = pcbnew.PCB_TRACK(board)
    t.SetStart(pcbnew.VECTOR2I(pcbnew.FromMM(x1), pcbnew.FromMM(y1)))
    t.SetEnd(pcbnew.VECTOR2I(pcbnew.FromMM(x2), pcbnew.FromMM(y2)))
    t.SetWidth(pcbnew.FromMM(width))
    t.SetLayer(pcbnew.F_Cu)
    t.SetNet(net(board, netname))
    board.Add(t)


def main():
    HIST.mkdir(exist_ok=True)
    src = HIST / "qfbms32_pre_route_filters.kicad_pcb"
    shutil.copy2(src, PCB)
    board = pcbnew.LoadBoard(str(PCB))

    # Park R_B1..33 along top edge (still netless) — frees y≈25–31 corridor
    for i in range(1, 34):
        fp = board.FindFootprintByReference(f"R_B{i}")
        if not fp:
            continue
        x = 35.0 + (i - 1) * 2.2
        if x > 120:
            x = 35.0 + (i - 17) * 2.2
            y = 3.5
        else:
            y = 1.8
        fp.SetPosition(pcbnew.VECTOR2I(pcbnew.FromMM(x), pcbnew.FromMM(y)))
        fp.SetOrientation(pcbnew.EDA_ANGLE(90, pcbnew.DEGREES_T))

    n = 0
    for k in range(1, 33):
        rf = board.FindFootprintByReference(f"R_F{k}")
        cell_n = 33 - k
        cell_net = f"CELL{cell_n}"
        cell_pad = next((p for p in rf.Pads() if p.GetNetname() == cell_net), None)
        if not cell_pad:
            continue
        jpad = None
        for cref in ("J_CELL1", "J_CELL2", "J_CELL3", "J_CELL4"):
            fp = board.FindFootprintByReference(cref)
            for p in fp.Pads():
                if p.GetNetname() == cell_net and str(p.GetNumber()).isdigit():
                    jpad = p
                    break
            if jpad:
                break
        if not jpad:
            continue
        jx = pcbnew.ToMM(jpad.GetPosition().x)
        jy = pcbnew.ToMM(jpad.GetPosition().y)
        cx = pcbnew.ToMM(cell_pad.GetPosition().x)
        cy = pcbnew.ToMM(cell_pad.GetPosition().y)
        # jog slightly so adjacent channels don't share the same y-run overlap on pads
        mid_y = (jy + cy) / 2
        add_track(board, jx, jy, jx, mid_y, cell_net)
        add_track(board, jx, mid_y, cx, mid_y, cell_net)
        add_track(board, cx, mid_y, cx, cy, cell_net)
        n += 1

    # BAT -> fuse short
    bat = board.FindFootprintByReference("J_BAT1").FindPadByNumber("1")
    f1 = board.FindFootprintByReference("F1")
    fpad = next(p for p in f1.Pads() if p.GetNetname() == "CELL32")
    ax, ay = pcbnew.ToMM(bat.GetPosition().x), pcbnew.ToMM(bat.GetPosition().y)
    bx, by = pcbnew.ToMM(fpad.GetPosition().x), pcbnew.ToMM(fpad.GetPosition().y)
    add_track(board, ax, ay, bx, ay, "CELL32", width=0.8)
    add_track(board, bx, ay, bx, by, "CELL32", width=0.8)

    pcbnew.SaveBoard(str(PCB), board)
    print(f"parked R_B*; routed {n} CELL stubs; saved {PCB}")


if __name__ == "__main__":
    main()
