"""Deterministic R_F monitor fanout. Track 0.2 mm, via 0.6 / 0.3 mm.

Does not move footprints. Does not route gates, the relay, or the power stage.
"""
from __future__ import annotations

import shutil
from pathlib import Path

import pcbnew

ROOT = Path(r"c:\Users\quinn\Documents\GitHub\Fungineers PCB designs\qfbms32 ai pcb")
PCB = ROOT / "qfbms32.kicad_pcb"
HIST = ROOT / ".history"
W = 0.2
VIA_D = 0.6
VIA_DRILL = 0.3
CLEAR = 0.127
HALF = W / 2
# via center to foreign track center
VIA_TRACK = VIA_D / 2 + CLEAR + HALF
PITCH = 0.60
TOP = 22.9


def mm(v):
    return pcbnew.ToMM(v)


def ensure_net(board, name):
    n = board.FindNet(name)
    if n is not None and n.GetNetCode() > 0:
        return n
    board.Add(pcbnew.NETINFO_ITEM(board, name))
    n = board.FindNet(name)
    if n is None or n.GetNetCode() <= 0:
        raise RuntimeError(name)
    return n


def box_of(pad):
    b = pad.GetBoundingBox()
    xs = (mm(b.GetLeft()), mm(b.GetRight()))
    ys = (mm(b.GetTop()), mm(b.GetBottom()))
    return (min(xs), min(ys), max(xs), max(ys))


def dist_box(x, y, box):
    x1, y1, x2, y2 = box
    dx = 0.0 if x1 <= x <= x2 else (x1 - x if x < x1 else x - x2)
    dy = 0.0 if y1 <= y <= y2 else (y1 - y if y < y1 else y - y2)
    return (dx * dx + dy * dy) ** 0.5


def seg_point_dist(px, py, x1, y1, x2, y2):
    dx, dy = x2 - x1, y2 - y1
    if dx == 0 and dy == 0:
        return ((px - x1) ** 2 + (py - y1) ** 2) ** 0.5
    t = ((px - x1) * dx + (py - y1) * dy) / (dx * dx + dy * dy)
    t = 0 if t < 0 else 1 if t > 1 else t
    return ((px - (x1 + t * dx)) ** 2 + (py - (y1 + t * dy)) ** 2) ** 0.5


class Geom:
    def __init__(self):
        # foreign and committed copper: (net, layer, x1, y1, x2, y2) layer 'F','B','V'
        self.rects = []
        self.segs = []  # net, layer, x1,y1,x2,y2, half
        self.vias = []  # net, x, y

    def add_pad(self, net, pad):
        x1, y1, x2, y2 = box_of(pad)
        if pad.IsOnLayer(pcbnew.B_Cu) and not pad.IsOnLayer(pcbnew.F_Cu):
            layer = "B"
        elif pad.IsOnLayer(pcbnew.F_Cu) and not pad.IsOnLayer(pcbnew.B_Cu):
            layer = "F"
        else:
            layer = "FB"
        self.rects.append((net, layer, x1, y1, x2, y2))

    def add_seg(self, net, layer, x1, y1, x2, y2):
        self.segs.append((net, layer, x1, y1, x2, y2, HALF))

    def add_via(self, net, x, y):
        self.vias.append((net, x, y))

    def track_ok(self, net, layer, x1, y1, x2, y2):
        hits = []
        for pnet, ply, a, b, c, d in self.rects:
            if pnet == net:
                continue
            if ply not in (layer, "FB", "V"):
                continue
            # sample
            steps = max(2, int(max(abs(x2 - x1), abs(y2 - y1)) / 0.15) + 1)
            for s in range(steps + 1):
                t = s / steps
                x = x1 + (x2 - x1) * t
                y = y1 + (y2 - y1) * t
                if dist_box(x, y, (a, b, c, d)) < HALF + CLEAR:
                    hits.append((pnet, round(x, 2), round(y, 2)))
                    return hits
        for snet, sly, a, b, c, d, half in self.segs:
            if snet == net or sly != layer:
                continue
            # centerline separation
            steps = max(2, int(max(abs(x2 - x1), abs(y2 - y1)) / 0.15) + 1)
            need = HALF + half + CLEAR
            for s in range(steps + 1):
                t = s / steps
                x = x1 + (x2 - x1) * t
                y = y1 + (y2 - y1) * t
                if seg_point_dist(x, y, a, b, c, d) < need - 1e-6:
                    hits.append((snet, round(x, 2), round(y, 2)))
                    return hits
        for vnet, vx, vy in self.vias:
            if vnet == net:
                continue
            if seg_point_dist(vx, vy, x1, y1, x2, y2) < VIA_TRACK - 1e-6:
                hits.append((vnet + ":via", round(vx, 2), round(vy, 2)))
                return hits
        return hits

    def via_ok(self, net, x, y):
        if not (0.7 < x < 129.3 and 0.7 < y < 31.5):
            return False
        for pnet, ply, a, b, c, d in self.rects:
            if pnet == net:
                continue
            if dist_box(x, y, (a, b, c, d)) < VIA_D / 2 + CLEAR:
                return False
        for snet, sly, a, b, c, d, half in self.segs:
            if snet == net:
                continue
            if seg_point_dist(x, y, a, b, c, d) < VIA_D / 2 + CLEAR + half:
                return False
        for vnet, vx, vy in self.vias:
            if (x - vx) ** 2 + (y - vy) ** 2 < (VIA_D + CLEAR) ** 2 - 1e-6:
                return False
        return True


def vc_num(cell_n):
    return cell_n if cell_n <= 16 else cell_n - 16


def pin_for(vc):
    if vc == 16:
        return 48
    if vc == 0:
        return 16
    return 16 - vc


def main():
    HIST.mkdir(exist_ok=True)
    backup = HIST / "qfbms32_pre_cell_fanout.kicad_pcb"
    shutil.copy2(PCB, backup)
    board = pcbnew.LoadBoard(str(PCB))
    frozen = {
        fp.GetReference(): (
            round(mm(fp.GetPosition().x), 4),
            round(mm(fp.GetPosition().y), 4),
            round(fp.GetOrientation().AsDegrees(), 3),
        )
        for fp in board.GetFootprints()
    }
    for ref, name in (("U_BQ1", "BQ1_BAT"), ("U_BQ2", "BQ2_BAT")):
        p = board.FindFootprintByReference(ref).FindPadByNumber("47")
        print(f"{ref} pin47 {p.GetNetname()} -> {name}")
        p.SetNet(ensure_net(board, name))

    g = Geom()
    for fp in board.GetFootprints():
        for pad in fp.Pads():
            g.add_pad(pad.GetNetname(), pad)
    for t in board.GetTracks():
        layer = "B" if t.GetLayer() == pcbnew.B_Cu else "F"
        g.add_seg(
            t.GetNetname(),
            layer,
            mm(t.GetStart().x),
            mm(t.GetStart().y),
            mm(t.GetEnd().x),
            mm(t.GetEnd().y),
        )

    groups = []
    for chip, k0 in (("U_BQ2", 1), ("U_BQ1", 17)):
        nets = []
        for k in range(k0, k0 + 16):
            rf = board.FindFootprintByReference(f"R_F{k}")
            mon = next(p for p in rf.Pads() if p.GetNumber() == "2")
            cell_n = 33 - k
            vc = vc_num(cell_n)
            bq = board.FindFootprintByReference(chip).FindPadByNumber(str(pin_for(vc)))
            if bq.GetNetname() != mon.GetNetname():
                raise RuntimeError(mon.GetNetname())
            caps = []
            for ci in range(1, 33):
                for pad in board.FindFootprintByReference(f"C_F{ci}").Pads():
                    if pad.GetNetname() == mon.GetNetname():
                        caps.append(pad)
            south = max(caps, key=lambda p: mm(p.GetPosition().y))
            nets.append({
                "net": mon.GetNetname(),
                "sx": mm(mon.GetPosition().x),
                "sy": mm(mon.GetPosition().y),
                "tx": mm(south.GetPosition().x),
                "ty": mm(south.GetPosition().y),
                "caps": caps,
                "bq": bq,
                "chip": chip,
            })
        groups.append(nets)

    problems = []
    drawn = []  # (net, kind, payload)

    def commit_seg(net, layer, x1, y1, x2, y2):
        if abs(x1 - x2) < 1e-6 and abs(y1 - y2) < 1e-6:
            return True
        hit = g.track_ok(net, layer, x1, y1, x2, y2)
        if hit:
            problems.append((net, layer, (round(x1, 2), round(y1, 2), round(x2, 2), round(y2, 2)), hit[0]))
            return False
        g.add_seg(net, layer, x1, y1, x2, y2)
        drawn.append((net, "seg", (layer, x1, y1, x2, y2)))
        return True

    def commit_via(net, x, y):
        if not g.via_ok(net, x, y):
            problems.append((net, "via", (round(x, 2), round(y, 2))))
            return False
        g.add_via(net, x, y)
        drawn.append((net, "via", (x, y)))
        return True

    for nets in groups:
        for i, n in enumerate(nets):
            n["lane"] = TOP - i * PITCH
        for i, n in enumerate(nets):
            net = n["net"]
            sx, sy, lane = n["sx"], n["sy"], n["lane"]
            tx = n["tx"]
            # which higher lanes does this source vertical cross?
            crossed = []
            for m in nets:
                if m["lane"] <= lane:
                    continue
                lo, hi = sorted((m["sx"], m["tx"]))
                if lo - 0.05 < sx < hi + 0.05:
                    crossed.append(m["lane"])
            ok = commit_via(net, sx, sy)
            if not crossed:
                ok = commit_seg(net, "B", sx, sy, sx, lane) and ok
            else:
                y_hi = max(crossed) + 0.62
                y_lo = min(crossed) - 0.62
                if y_hi > 23.35:
                    y_hi = 23.35
                dx = None
                for trial in [0.0, 0.4, -0.4, 0.7, -0.7, 1.0, -1.0]:
                    x = sx + trial
                    if any(abs(x - m["sx"]) < 0.5 and m is not n for m in nets):
                        continue
                    if g.track_ok(net, "F", x, y_lo, x, y_hi):
                        continue
                    if g.via_ok(net, x, y_hi) and g.via_ok(net, x, y_lo):
                        dx = trial
                        break
                if dx is None:
                    problems.append((net, "no-fcu-column", (round(sx, 2), round(y_lo, 2), round(y_hi, 2))))
                    dx = 0.0
                x = sx + dx
                ok = commit_seg(net, "B", sx, sy, sx, y_hi) and ok
                if abs(dx) > 1e-6:
                    ok = commit_seg(net, "B", sx, y_hi, x, y_hi) and ok
                ok = commit_via(net, x, y_hi) and ok
                ok = commit_seg(net, "F", x, y_hi, x, y_lo) and ok
                ok = commit_via(net, x, y_lo) and ok
                if abs(dx) > 1e-6:
                    ok = commit_seg(net, "B", x, y_lo, sx, y_lo) and ok
                ok = commit_seg(net, "B", sx, y_lo, sx, lane) and ok
            ok = commit_seg(net, "B", sx, lane, tx, lane) and ok
            # drop on B.Cu just above the caps. Lower lanes are crossed;
            # those spans are jumped on F.Cu at tx if a clear column exists.
            span_lo = []
            for m in nets:
                if m["lane"] >= lane - 0.01:
                    continue
                lo, hi = sorted((m["sx"], m["tx"]))
                if lo - 0.05 < tx < hi + 0.05:
                    span_lo.append(m["lane"])
            if not span_lo:
                ok = commit_seg(net, "B", tx, lane, tx, n["ty"]) and ok
            else:
                yb = max(14.75, min(span_lo) - 0.62)
                dx = None
                for trial in [0.0, 0.45, -0.45, 0.9, -0.9, 1.3, -1.3, 1.7, -1.7]:
                    x = tx + trial
                    if g.track_ok(net, "F", x, yb, x, lane):
                        continue
                    if g.via_ok(net, x, lane) and g.via_ok(net, x, yb):
                        dx = trial
                        break
                if dx is None:
                    problems.append((net, "no-drop", (round(tx, 2), round(lane, 2), round(yb, 2))))
                    ok = False
                    dx = 0.0
                x = tx + dx
                if abs(dx) > 1e-6:
                    ok = commit_seg(net, "B", tx, lane, x, lane) and ok
                ok = commit_via(net, x, lane) and ok
                ok = commit_seg(net, "F", x, lane, x, yb) and ok
                ok = commit_via(net, x, yb) and ok
                if abs(dx) > 1e-6:
                    ok = commit_seg(net, "B", x, yb, tx, yb) and ok
                ok = commit_seg(net, "B", tx, yb, tx, n["ty"]) and ok
            for pad in n["caps"]:
                px, py = mm(pad.GetPosition().x), mm(pad.GetPosition().y)
                if abs(px - tx) < 0.05 and abs(py - n["ty"]) < 0.05:
                    continue
                mid = (tx + px) / 2
                ok = commit_seg(net, "B", tx, n["ty"], mid, n["ty"]) and ok
                ok = commit_seg(net, "B", mid, n["ty"], mid, py) and ok
                ok = commit_seg(net, "B", mid, py, px, py) and ok
            n["ok"] = ok

    # BQ pin escapes. Search a via just outside the pad, F.Cu onto the pad,
    # B.Cu from that via to the south cap pad along a private offset.
    for nets in groups:
        for n in nets:
            pin = n["bq"]
            x1, y1, x2, y2 = box_of(pin)
            cx, cy = (x1 + x2) / 2, (y1 + y2) / 2
            chip_x = 44.8 if n["chip"] == "U_BQ2" else 87.9
            if (x2 - x1) > (y2 - y1):
                direction = (-1, 0) if cx < chip_x else (1, 0)
            else:
                direction = (0, -1) if cy < 14 else (0, 1)
            found = None
            for dist in (1.1, 1.5, 1.9, 2.4, 3.0, 3.6, 4.2):
                for lat in (0.0, 0.55, -0.55, 1.1, -1.1, 1.6, -1.6):
                    vx = cx + direction[0] * dist - direction[1] * lat
                    vy = cy + direction[1] * dist + direction[0] * lat
                    if g.via_ok(n["net"], vx, vy) and not g.track_ok(n["net"], "F", vx, vy, cx, cy):
                        found = (vx, vy)
                        break
                if found:
                    break
            if not found:
                problems.append((n["net"], "no-pin-via", (round(cx, 2), round(cy, 2))))
                continue
            vx, vy = found
            commit_via(n["net"], vx, vy)
            commit_seg(n["net"], "F", vx, vy, cx, cy)
            # B.Cu from via to south pad: two-segment, preferring a Y south of the caps
            commit_seg(n["net"], "B", vx, vy, vx, 14.15)
            commit_seg(n["net"], "B", vx, 14.15, n["tx"], 14.15)
            commit_seg(n["net"], "B", n["tx"], 14.15, n["tx"], n["ty"])

    print("problems", len(problems))
    for row in problems[:40]:
        print(" ", row)
    moved = []
    for ref, pos in frozen.items():
        fp = board.FindFootprintByReference(ref)
        now = (
            round(mm(fp.GetPosition().x), 4),
            round(mm(fp.GetPosition().y), 4),
            round(fp.GetOrientation().AsDegrees(), 3),
        )
        if now != pos:
            moved.append(ref)
    if moved:
        raise RuntimeError(moved)
    if problems:
        print("not saved")
        return

    for net_name, kind, payload in drawn:
        net = ensure_net(board, net_name)
        if kind == "via":
            x, y = payload
            v = pcbnew.PCB_VIA(board)
            v.SetPosition(pcbnew.VECTOR2I(pcbnew.FromMM(x), pcbnew.FromMM(y)))
            v.SetWidth(pcbnew.FromMM(VIA_D))
            v.SetDrill(pcbnew.FromMM(VIA_DRILL))
            v.SetViaType(pcbnew.VIATYPE_THROUGH)
            v.SetLayerPair(pcbnew.F_Cu, pcbnew.B_Cu)
            v.SetNet(net)
            board.Add(v)
        else:
            layer, x1, y1, x2, y2 = payload
            t = pcbnew.PCB_TRACK(board)
            t.SetStart(pcbnew.VECTOR2I(pcbnew.FromMM(x1), pcbnew.FromMM(y1)))
            t.SetEnd(pcbnew.VECTOR2I(pcbnew.FromMM(x2), pcbnew.FromMM(y2)))
            t.SetWidth(pcbnew.FromMM(W))
            t.SetLayer(pcbnew.B_Cu if layer == "B" else pcbnew.F_Cu)
            t.SetNet(net)
            board.Add(t)
    pcbnew.SaveBoard(str(PCB), board)
    print("saved", len(drawn), "items")


if __name__ == "__main__":
    main()
