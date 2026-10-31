"""R_F pad 2 -> via -> B.Cu lane -> C_F and BQ pin.

Vias are 0.6 mm diameter, 0.3 mm drill. Filter tracks are 0.2 mm.
Footprints are not moved.
"""
from __future__ import annotations

import shutil
from pathlib import Path

import pcbnew

ROOT = Path(r"c:\Users\quinn\Documents\GitHub\Fungineers PCB designs\qfbms32 ai pcb")
PCB = ROOT / "qfbms32.kicad_pcb"
W, VIA_D, VIA_DRILL = 0.2, 0.6, 0.3
CLEAR = 0.10
HALF = 0.1
VIA_R = 0.3


def mm(v):
    return pcbnew.ToMM(v)


def ensure(board, name):
    n = board.FindNet(name)
    if n is not None and n.GetNetCode() > 0:
        return n
    board.Add(pcbnew.NETINFO_ITEM(board, name))
    return board.FindNet(name)


def box(pad):
    b = pad.GetBoundingBox()
    xs = (mm(b.GetLeft()), mm(b.GetRight()))
    ys = (mm(b.GetTop()), mm(b.GetBottom()))
    return min(xs), min(ys), max(xs), max(ys)


def db(x, y, r):
    a, b, c, d = r
    dx = 0 if a <= x <= c else (a - x if x < a else x - c)
    dy = 0 if b <= y <= d else (b - y if y < b else y - d)
    return (dx * dx + dy * dy) ** 0.5


def sd(px, py, x1, y1, x2, y2):
    dx, dy = x2 - x1, y2 - y1
    if dx == 0 and dy == 0:
        return ((px - x1) ** 2 + (py - y1) ** 2) ** 0.5
    t = max(0, min(1, ((px - x1) * dx + (py - y1) * dy) / (dx * dx + dy * dy)))
    return ((px - x1 - t * dx) ** 2 + (py - y1 - t * dy) ** 2) ** 0.5


class G:
    def __init__(self):
        self.rects = []
        self.segs = []
        self.vias = []

    def pad(self, net, p):
        layer = "B" if p.IsOnLayer(pcbnew.B_Cu) and not p.IsOnLayer(pcbnew.F_Cu) else "F"
        self.rects.append((net, layer, box(p)))

    def seg(self, net, layer, x1, y1, x2, y2):
        self.segs.append((net, layer, x1, y1, x2, y2))

    def via(self, net, x, y):
        self.vias.append((net, x, y))

    def seg_ok(self, net, layer, x1, y1, x2, y2):
        n = max(2, int(max(abs(x2 - x1), abs(y2 - y1)) / 0.2) + 1)
        for s in range(n + 1):
            t = s / n
            x, y = x1 + (x2 - x1) * t, y1 + (y2 - y1) * t
            for pn, pl, r in self.rects:
                if pn == net or pl != layer:
                    continue
                if db(x, y, r) < HALF + CLEAR:
                    return False
            for sn, sl, a, b, c, d in self.segs:
                if sn == net or sl != layer:
                    continue
                if sd(x, y, a, b, c, d) < W + CLEAR:
                    return False
            for vn, vx, vy in self.vias:
                if vn == net:
                    continue
                if sd(vx, vy, x1, y1, x2, y2) < VIA_R + CLEAR + HALF:
                    return False
        return True

    def via_ok(self, net, x, y):
        if not (0.8 < x < 129.2 and 0.8 < y < 31.6):
            return False
        for pn, pl, r in self.rects:
            if pn == net:
                continue
            if db(x, y, r) < VIA_R + CLEAR:
                return False
        for sn, sl, a, b, c, d in self.segs:
            if sn == net:
                continue
            if sd(x, y, a, b, c, d) < VIA_R + CLEAR + HALF:
                return False
        for vn, vx, vy in self.vias:
            if (x - vx) ** 2 + (y - vy) ** 2 < (VIA_D + CLEAR) ** 2:
                return False
        return True


def add_seg(board, g, net, layer, x1, y1, x2, y2):
    if abs(x1 - x2) < 1e-4 and abs(y1 - y2) < 1e-4:
        return True
    if not g.seg_ok(net, layer, x1, y1, x2, y2):
        return False
    t = pcbnew.PCB_TRACK(board)
    t.SetStart(pcbnew.VECTOR2I(pcbnew.FromMM(x1), pcbnew.FromMM(y1)))
    t.SetEnd(pcbnew.VECTOR2I(pcbnew.FromMM(x2), pcbnew.FromMM(y2)))
    t.SetWidth(pcbnew.FromMM(W))
    t.SetLayer(pcbnew.B_Cu if layer == "B" else pcbnew.F_Cu)
    t.SetNet(ensure(board, net))
    board.Add(t)
    g.seg(net, layer, x1, y1, x2, y2)
    return True


def add_via(board, g, net, x, y):
    if not g.via_ok(net, x, y):
        return False
    v = pcbnew.PCB_VIA(board)
    v.SetPosition(pcbnew.VECTOR2I(pcbnew.FromMM(x), pcbnew.FromMM(y)))
    v.SetWidth(pcbnew.FromMM(VIA_D))
    v.SetDrill(pcbnew.FromMM(VIA_DRILL))
    v.SetViaType(pcbnew.VIATYPE_THROUGH)
    v.SetLayerPair(pcbnew.F_Cu, pcbnew.B_Cu)
    v.SetNet(ensure(board, net))
    board.Add(v)
    g.via(net, x, y)
    return True


def main():
    board = pcbnew.LoadBoard(str(PCB))
    hist = ROOT / ".history"
    hist.mkdir(exist_ok=True)
    shutil.copy2(PCB, hist / "qfbms32_pre_cell_fanout.kicad_pcb")
    frozen = {
        fp.GetReference(): (round(mm(fp.GetPosition().x), 3), round(mm(fp.GetPosition().y), 3), round(fp.GetOrientation().AsDegrees(), 2))
        for fp in board.GetFootprints()
    }
    for ref, name in (("U_BQ1", "BQ1_BAT"), ("U_BQ2", "BQ2_BAT")):
        board.FindFootprintByReference(ref).FindPadByNumber("47").SetNet(ensure(board, name))
        print(ref, "pin47", name, "pin48", board.FindFootprintByReference(ref).FindPadByNumber("48").GetNetname())
    # Gate is pad 1 on the AGM drawing. Pad 4 is a source.
    board.FindFootprintByReference("Q1").FindPadByNumber("1").SetNet(ensure(board, "Q1_GATE"))
    board.FindFootprintByReference("Q1").FindPadByNumber("4").SetNet(ensure(board, "CHG+"))
    board.FindFootprintByReference("Q2").FindPadByNumber("1").SetNet(ensure(board, "Q2_GATE"))
    board.FindFootprintByReference("Q2").FindPadByNumber("4").SetNet(ensure(board, "PACK+"))

    g = G()
    for fp in board.GetFootprints():
        for p in fp.Pads():
            g.pad(p.GetNetname(), p)
    for t in board.GetTracks():
        g.seg(t.GetNetname(), "B" if t.GetLayer() == pcbnew.B_Cu else "F", mm(t.GetStart().x), mm(t.GetStart().y), mm(t.GetEnd().x), mm(t.GetEnd().y))

    # gaps between R_B pads, x centers
    gaps = []
    rbs = []
    for i in range(1, 34):
        fp = board.FindFootprintByReference(f"R_B{i}")
        xs = []
        for p in fp.Pads():
            a, b, c, d = box(p)
            xs += [a, c]
        rbs.append((min(xs), max(xs)))
    rbs.sort()
    for (a1, b1), (a2, b2) in zip(rbs, rbs[1:]):
        if a2 > b1:
            gaps.append((b1 + a2) / 2)

    def nearest_gap(sx, cell_pad):
        # Stay in the R_B gap beside this resistor, off the cell-side pad.
        a, _b, c, _d = box(cell_pad)
        edge = max(a, c)
        # 0.2 mm track, 0.10 mm off that pad, biased into the gap toward the monitor pad
        return edge + HALF + CLEAR + 0.06

    fail = []
    for chip, k0 in (("U_BQ2", 1), ("U_BQ1", 17)):
        group = []
        for k in range(k0, k0 + 16):
            rf = board.FindFootprintByReference(f"R_F{k}")
            mon = next(p for p in rf.Pads() if p.GetNumber() == "2")
            cellpad = next(p for p in rf.Pads() if p.GetNumber() == "1")
            cell = 33 - k
            vc = cell if cell <= 16 else cell - 16
            bq = board.FindFootprintByReference(chip).FindPadByNumber("48" if vc == 16 else str(16 - vc))
            caps = [p for n in range(1, 33) for p in board.FindFootprintByReference(f"C_F{n}").Pads() if p.GetNetname() == mon.GetNetname()]
            south = max(caps, key=lambda p: mm(p.GetPosition().y))
            group.append({
                "net": mon.GetNetname(),
                "sx": mm(mon.GetPosition().x),
                "sy": mm(mon.GetPosition().y),
                "tx": mm(south.GetPosition().x),
                "ty": mm(south.GetPosition().y),
                "caps": caps,
                "bq": bq,
                "cellpad": cellpad,
            })
        for i, n in enumerate(group):
            n["lane"] = 25.4 - i * 0.58
            n["gx"] = nearest_gap(n["sx"], n["cellpad"])
        for n in group:
            net, sx, sy, gx, lane = n["net"], n["sx"], n["sy"], n["gx"], n["lane"]
            tx, ty = n["tx"], n["ty"]
            steps = [
                ("via", sx, sy),
                ("F", sx, sy, gx, sy),
                ("F", gx, sy, gx, 28.08),
                ("via", gx, 28.08),
                ("B", gx, 28.08, gx, 26.12),
                ("via", gx, 26.12),
                ("F", gx, 26.12, gx, lane),
                ("via", gx, lane),
                ("B", gx, lane, tx, lane),
                ("B", tx, lane, tx, ty),
            ]
            # other cap pads through the gap between the columns
            for p in n["caps"]:
                px, py = mm(p.GetPosition().x), mm(p.GetPosition().y)
                if abs(px - tx) < 0.08 and abs(py - ty) < 0.08:
                    continue
                mid = (tx + px) / 2.0
                steps += [
                    ("B", tx, ty, mid, ty),
                    ("B", mid, ty, mid, py),
                    ("B", mid, py, px, py),
                ]
            bad = False
            for st in steps:
                if st[0] == "via":
                    ok = add_via(board, g, net, st[1], st[2])
                else:
                    ok = add_seg(board, g, net, st[0], st[1], st[2], st[3], st[4])
                if not ok:
                    fail.append((net, st[0], tuple(round(v, 2) for v in st[1:])))
                    bad = True
                    break
            print(("FAIL " if bad else "OK   ") + net)

    moved = []
    for ref, pos in frozen.items():
        fp = board.FindFootprintByReference(ref)
        now = (round(mm(fp.GetPosition().x), 3), round(mm(fp.GetPosition().y), 3), round(fp.GetOrientation().AsDegrees(), 2))
        if now != pos:
            moved.append(ref)
    if moved:
        raise RuntimeError(moved)
    print("failures", len(fail))
    for row in fail[:25]:
        print(" ", row)
    if fail:
        print("not saved")
        return
    pcbnew.SaveBoard(str(PCB), board)
    print("saved")


if __name__ == "__main__":
    main()
