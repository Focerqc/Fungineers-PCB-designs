"""
Safe cell stubs only: J_CELL pad -> R_F cell-side pad on F.Cu.
No vias / B.Cu fanout (those crossed under dense BQ areas).
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
    # Start from pre-route (nets + SSR stubs only)
    src = HIST / "qfbms32_pre_route_filters.kicad_pcb"
    shutil.copy2(src, PCB)
    shutil.copy2(PCB, HIST / "qfbms32_pre_cell_stubs.kicad_pcb")
    board = pcbnew.LoadBoard(str(PCB))

    n = 0
    for k in range(1, 33):
        rf = board.FindFootprintByReference(f"R_F{k}")
        cell_n = 33 - k
        cell_net = f"CELL{cell_n}"
        cell_pad = None
        for p in rf.Pads():
            if p.GetNetname() == cell_net:
                cell_pad = p
                break
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
        jx, jy = pcbnew.ToMM(jpad.GetPosition().x), pcbnew.ToMM(jpad.GetPosition().y)
        cx, cy = pcbnew.ToMM(cell_pad.GetPosition().x), pcbnew.ToMM(cell_pad.GetPosition().y)
        # Vertical then horizontal — R_F is below connectors (larger Y)
        add_track(board, jx, jy, jx, cy, cell_net)
        add_track(board, jx, cy, cx, cy, cell_net)
        n += 1

    # Minimal power stubs that are short / local
    def pad(ref, netname=None, pnum=None):
        fp = board.FindFootprintByReference(ref)
        for p in fp.Pads():
            if pnum is not None and p.GetNumber() != pnum:
                continue
            if netname is not None and p.GetNetname() != netname:
                continue
            return p
        return None

    # F1 between BAT and fused — short
    a, b = pad("J_BAT1", "CELL32", "1"), pad("F1", "CELL32")
    if a and b:
        ax, ay = pcbnew.ToMM(a.GetPosition().x), pcbnew.ToMM(a.GetPosition().y)
        bx, by = pcbnew.ToMM(b.GetPosition().x), pcbnew.ToMM(b.GetPosition().y)
        add_track(board, ax, ay, bx, ay, "CELL32", width=0.8)
        add_track(board, bx, ay, bx, by, "CELL32", width=0.8)

    pcbnew.SaveBoard(str(PCB), board)
    print(f"cell stubs {n}; board {PCB}")


if __name__ == "__main__":
    main()
