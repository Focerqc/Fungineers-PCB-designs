"""
Stub-route power stage nets: TOP_CELL/CELL32, fuse, FETs, CHG±, shunt, SSR gate.
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


def add_track(board, x1, y1, x2, y2, netname, width=0.5, layer=pcbnew.F_Cu):
    if abs(x1 - x2) < 1e-6 and abs(y1 - y2) < 1e-6:
        return
    t = pcbnew.PCB_TRACK(board)
    t.SetStart(pcbnew.VECTOR2I(pcbnew.FromMM(x1), pcbnew.FromMM(y1)))
    t.SetEnd(pcbnew.VECTOR2I(pcbnew.FromMM(x2), pcbnew.FromMM(y2)))
    t.SetWidth(pcbnew.FromMM(width))
    t.SetLayer(layer)
    t.SetNet(net(board, netname))
    board.Add(t)


def pad_xy(pad):
    p = pad.GetPosition()
    return pcbnew.ToMM(p.x), pcbnew.ToMM(p.y)


def first_pad(board, ref, netname=None, pnum=None):
    fp = board.FindFootprintByReference(ref)
    if not fp:
        return None
    for p in fp.Pads():
        if pnum is not None and p.GetNumber() != pnum:
            continue
        if netname is not None and p.GetNetname() != netname:
            continue
        return p
    return None


def main():
    HIST.mkdir(exist_ok=True)
    shutil.copy2(PCB, HIST / "qfbms32_pre_route_power.kicad_pcb")
    board = pcbnew.LoadBoard(str(PCB))

    # J_BAT1 pad1 CELL32 -> F1 pad1
    a = first_pad(board, "J_BAT1", "CELL32", "1")
    b = first_pad(board, "F1", "CELL32")
    if a and b:
        ax, ay = pad_xy(a)
        bx, by = pad_xy(b)
        add_track(board, ax, ay, bx, ay, "CELL32", width=1.0)
        add_track(board, bx, ay, bx, by, "CELL32", width=1.0)

    # F1 fused -> Q1/Q2 drains
    f2 = first_pad(board, "F1", "CELL32_FUSED")
    q1d = first_pad(board, "Q1", "CELL32_FUSED", "D")
    q2d = first_pad(board, "Q2", "CELL32_FUSED", "D")
    if f2 and q1d:
        fx, fy = pad_xy(f2)
        qx, qy = pad_xy(q1d)
        add_track(board, fx, fy, qx, fy, "CELL32_FUSED", width=1.0)
        add_track(board, qx, fy, qx, qy, "CELL32_FUSED", width=1.0)
    if f2 and q2d:
        fx, fy = pad_xy(f2)
        qx, qy = pad_xy(q2d)
        add_track(board, fx, fy, fx, qy, "CELL32_FUSED", width=0.8)
        add_track(board, fx, qy, qx, qy, "CELL32_FUSED", width=0.8)

    # Q1 source CHG+ -> J_CHG1
    q1s = first_pad(board, "Q1", "CHG+", "1")
    jchg = first_pad(board, "J_CHG1", "CHG+", "1")
    if q1s and jchg:
        sx, sy = pad_xy(q1s)
        jx, jy = pad_xy(jchg)
        add_track(board, sx, sy, jx, sy, "CHG+", width=1.0)
        add_track(board, jx, sy, jx, jy, "CHG+", width=1.0)

    # Shunt: J_BAT1 CELL0 -> R_SH1 -> R_SH2 -> J_CHG1 CHG-
    bat0 = first_pad(board, "J_BAT1", "CELL0", "2")
    sh1a = first_pad(board, "R_SH1", "CELL0")
    sh1b = first_pad(board, "R_SH1", "SHUNT_MID")
    sh2a = first_pad(board, "R_SH2", "SHUNT_MID")
    sh2b = first_pad(board, "R_SH2", "CHG-")
    chgm = first_pad(board, "J_CHG1", "CHG-", "2")
    if bat0 and sh1a:
        x1, y1 = pad_xy(bat0)
        x2, y2 = pad_xy(sh1a)
        add_track(board, x1, y1, x2, y1, "CELL0", width=1.0)
        add_track(board, x2, y1, x2, y2, "CELL0", width=1.0)
    if sh1b and sh2a:
        x1, y1 = pad_xy(sh1b)
        x2, y2 = pad_xy(sh2a)
        add_track(board, x1, y1, x2, y1, "SHUNT_MID", width=0.8)
        add_track(board, x2, y1, x2, y2, "SHUNT_MID", width=0.8)
    if sh2b and chgm:
        x1, y1 = pad_xy(sh2b)
        x2, y2 = pad_xy(chgm)
        add_track(board, x1, y1, x2, y1, "CHG-", width=1.0)
        add_track(board, x2, y1, x2, y2, "CHG-", width=1.0)

    # Gate: U_SSR1 OUT_CHG -> R_SSR1 -> Q1_GATE cluster (already partially netted)
    ssr8 = first_pad(board, "U_SSR1", "SSR_OUT_CHG", "8")
    r1 = first_pad(board, "R_SSR1", "SSR_OUT_CHG")
    if ssr8 and r1:
        x1, y1 = pad_xy(ssr8)
        x2, y2 = pad_xy(r1)
        add_track(board, x1, y1, x2, y1, "SSR_OUT_CHG", width=0.25)
        add_track(board, x2, y1, x2, y2, "SSR_OUT_CHG", width=0.25)

    r1g = first_pad(board, "R_SSR1", "Q1_GATE")
    q1g = first_pad(board, "Q1", "Q1_GATE", "4")
    if r1g and q1g:
        x1, y1 = pad_xy(r1g)
        x2, y2 = pad_xy(q1g)
        add_track(board, x1, y1, x2, y1, "Q1_GATE", width=0.25)
        add_track(board, x2, y1, x2, y2, "Q1_GATE", width=0.25)

    pcbnew.SaveBoard(str(PCB), board)
    print("Power stage stubs saved", PCB)


if __name__ == "__main__":
    main()
