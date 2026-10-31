"""Cell-filter fanout and the power-stage nets.

Track 0.2 mm on the filter. Via drill 0.3 mm, diameter 0.6 mm.
Q1/Q2 pad 1 is the gate (AGM15T03LL drawing). Pad 4 joins the source.
U_SSR1 pads 4 and 5 stay GND and VBOOST. Pads 7 and 8 stay the two outputs.
Does not move footprints.
"""
from __future__ import annotations

import heapq
import shutil
from pathlib import Path

import pcbnew

ROOT = Path(r"c:\Users\quinn\Documents\GitHub\Fungineers PCB designs\qfbms32 ai pcb")
PCB = ROOT / "qfbms32.kicad_pcb"
HIST = ROOT / ".history"

W = 0.2
VIA_D = 0.6
VIA_DRILL = 0.3
CLEAR = 0.15
HALF = W / 2
VIA_R = VIA_D / 2
OX, OY, P = 33.0, 8.0, 0.1
X1, Y1 = 106.0, 21.4
NX = int(round((X1 - OX) / P)) + 1
NY = int(round((Y1 - OY) / P)) + 1
TRUNK_Y = 16.6


def mm(v):
    return pcbnew.ToMM(v)


def ensure(board, name):
    n = board.FindNet(name)
    if n is not None and n.GetNetCode() > 0:
        return n
    board.Add(pcbnew.NETINFO_ITEM(board, name))
    n = board.FindNet(name)
    if n is None or n.GetNetCode() <= 0:
        raise RuntimeError(name)
    return n


def box(pad):
    b = pad.GetBoundingBox()
    xs = (mm(b.GetLeft()), mm(b.GetRight()))
    ys = (mm(b.GetTop()), mm(b.GetBottom()))
    return min(xs), min(ys), max(xs), max(ys)


def on_b(pad):
    return pad.IsOnLayer(pcbnew.B_Cu) and not pad.IsOnLayer(pcbnew.F_Cu)


def ij(x, y):
    return int(round((x - OX) / P)), int(round((y - OY) / P))


def xy(i, j):
    return OX + i * P, OY + j * P


def inside(i, j):
    return 0 <= i < NX and 0 <= j < NY


def dist_box(x, y, rect):
    a, b, c, d = rect
    dx = 0.0 if a <= x <= c else (a - x if x < a else x - c)
    dy = 0.0 if b <= y <= d else (b - y if y < b else y - d)
    return (dx * dx + dy * dy) ** 0.5


class World:
    def __init__(self):
        self.rects = []  # net, layer 0/1/2, box
        self.vias = []

    def add_pad(self, net, pad):
        layer = 0 if on_b(pad) else (1 if pad.IsOnLayer(pcbnew.F_Cu) else 2)
        self.rects.append((net, layer, box(pad)))

    def add_seg(self, net, layer, x1, y1, x2, y2, half):
        self.rects.append((net, layer, (min(x1, x2) - half, min(y1, y2) - half, max(x1, x2) + half, max(y1, y2) + half)))

    def add_via(self, net, x, y):
        self.vias.append((net, x, y))
        self.rects.append((net, 2, (x - VIA_R, y - VIA_R, x + VIA_R, y + VIA_R)))

    def raster(self, net, home_x):
        block = [bytearray(NX * NY), bytearray(NX * NY)]
        via_no = bytearray(NX * NY)
        keep = HALF + CLEAR
        vkeep = VIA_R + CLEAR
        for pnet, layer, (a, b, c, d) in self.rects:
            if pnet == net:
                continue
            layers = (0, 1) if layer == 2 else (layer,)
            i0, j0 = ij(a - keep, b - keep)
            i1, j1 = ij(c + keep, d + keep)
            vi0, vj0 = ij(a - vkeep, b - vkeep)
            vi1, vj1 = ij(c + vkeep, d + vkeep)
            for ly in layers:
                for j in range(max(0, min(j0, j1)), min(NY, max(j0, j1) + 1)):
                    y = OY + j * P
                    if y < b - keep or y > d + keep:
                        continue
                    row = j * NX
                    for i in range(max(0, min(i0, i1)), min(NX, max(i0, i1) + 1)):
                        x = OX + i * P
                        if a - keep <= x <= c + keep:
                            block[ly][row + i] = 1
            for j in range(max(0, min(vj0, vj1)), min(NY, max(vj0, vj1) + 1)):
                y = OY + j * P
                if y < b - vkeep or y > d + vkeep:
                    continue
                row = j * NX
                for i in range(max(0, min(vi0, vi1)), min(NX, max(vi0, vi1) + 1)):
                    x = OX + i * P
                    if a - vkeep <= x <= c + vkeep:
                        via_no[row + i] = 1
        for vnet, vx, vy in self.vias:
            if vnet == net:
                continue
            i0, j0 = ij(vx - (VIA_D + CLEAR), vy - (VIA_D + CLEAR))
            i1, j1 = ij(vx + (VIA_D + CLEAR), vy + (VIA_D + CLEAR))
            for j in range(max(0, j0), min(NY, j1 + 1)):
                row = j * NX
                y = OY + j * P
                for i in range(max(0, i0), min(NX, i1 + 1)):
                    x = OX + i * P
                    if (x - vx) ** 2 + (y - vy) ** 2 < (VIA_D + CLEAR) ** 2:
                        via_no[row + i] = 1
                        block[0][row + i] = 1
                        block[1][row + i] = 1
        # other people's trunks stay exclusive
        return block, via_no, home_x


def cells(pad):
    a, b, c, d = box(pad)
    layer = 0 if on_b(pad) else 1
    i0, j0 = ij(a, b)
    i1, j1 = ij(c, d)
    out = []
    for j in range(max(0, min(j0, j1)), min(NY, max(j0, j1) + 1)):
        for i in range(max(0, min(i0, i1)), min(NX, max(i0, i1) + 1)):
            x, y = xy(i, j)
            if a <= x <= c and b <= y <= d:
                out.append((i, j, layer))
    if not out:
        i, j = ij((a + c) / 2, (b + d) / 2)
        if inside(i, j):
            out.append((i, j, layer))
    return out


def astar(starts, goals, block, via_no, home_x):
    if not goals:
        return None
    gl = list(goals)
    gscore = {}
    parent = {}
    heap = []
    hi = ij(home_x, 0)[0]
    for s in starts:
        gscore[s] = 0
        parent[s] = None
        heapq.heappush(heap, (0, 0, s))
    found = None
    nexp = 0
    while heap:
        f, g, cur = heapq.heappop(heap)
        if g != gscore.get(cur):
            continue
        if cur in goals:
            found = cur
            break
        nexp += 1
        if nexp > 160000:
            return None
        i, j, layer = cur
        base = 1 if layer == 0 else 3
        for di, dj in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            ni, nj = i + di, j + dj
            if not inside(ni, nj) or block[layer][nj * NX + ni]:
                continue
            y = OY + nj * P
            if y > TRUNK_Y - 0.15 and abs((OX + ni * P) - home_x) > 0.45:
                continue
            nxt = (ni, nj, layer)
            ng = g + base
            if ng < gscore.get(nxt, 1 << 30):
                gscore[nxt] = ng
                parent[nxt] = (cur, 0)
                h = min(abs(ni - a) + abs(nj - b) for a, b, _c in gl)
                heapq.heappush(heap, (ng + h, ng, nxt))
        if not via_no[j * NX + i] and not block[1 - layer][j * NX + i]:
            nxt = (i, j, 1 - layer)
            ng = g + 12
            if ng < gscore.get(nxt, 1 << 30):
                gscore[nxt] = ng
                parent[nxt] = (cur, 1)
                h = min(abs(i - a) + abs(j - b) for a, b, _c in gl)
                heapq.heappush(heap, (ng + h, ng, nxt))
    if found is None:
        return None
    path = []
    cur = found
    while cur is not None:
        prev = parent.get(cur)
        path.append(cur)
        cur = None if prev is None else prev[0]
    path.reverse()
    return path, parent


def emit(path, parent):
    segs, vias = [], []
    cx, cy = xy(*path[0][:2])
    cl = path[0][2]
    px, py = cx, cy
    for cur in path[1:]:
        i, j, layer = cur
        x, y = xy(i, j)
        via = parent[cur][1]
        if via or layer != cl:
            if abs(px - cx) > 1e-9 or abs(py - cy) > 1e-9:
                segs.append((cl, cx, cy, px, py))
            vias.append((x, y))
            cx, cy, cl = x, y, layer
            px, py = x, y
        elif (abs(x - px) < 1e-9 and abs(px - cx) < 1e-9) or (abs(y - py) < 1e-9 and abs(py - cy) < 1e-9):
            px, py = x, y
        else:
            segs.append((cl, cx, cy, px, py))
            cx, cy, px, py, cl = px, py, x, y, layer
    if abs(px - cx) > 1e-9 or abs(py - cy) > 1e-9:
        segs.append((cl, cx, cy, px, py))
    return segs, vias


def put_track(board, world, netname, layer, x1, y1, x2, y2, width=W):
    if abs(x1 - x2) < 1e-6 and abs(y1 - y2) < 1e-6:
        return
    t = pcbnew.PCB_TRACK(board)
    t.SetStart(pcbnew.VECTOR2I(pcbnew.FromMM(x1), pcbnew.FromMM(y1)))
    t.SetEnd(pcbnew.VECTOR2I(pcbnew.FromMM(x2), pcbnew.FromMM(y2)))
    t.SetWidth(pcbnew.FromMM(width))
    t.SetLayer(pcbnew.B_Cu if layer == 0 else pcbnew.F_Cu)
    t.SetNet(ensure(board, netname))
    board.Add(t)
    world.add_seg(netname, layer, x1, y1, x2, y2, width / 2)


def put_via(board, world, netname, x, y):
    v = pcbnew.PCB_VIA(board)
    v.SetPosition(pcbnew.VECTOR2I(pcbnew.FromMM(x), pcbnew.FromMM(y)))
    v.SetWidth(pcbnew.FromMM(VIA_D))
    v.SetDrill(pcbnew.FromMM(VIA_DRILL))
    v.SetViaType(pcbnew.VIATYPE_THROUGH)
    v.SetLayerPair(pcbnew.F_Cu, pcbnew.B_Cu)
    v.SetNet(ensure(board, netname))
    board.Add(v)
    world.add_via(netname, x, y)


def setpad(board, ref, num, netname):
    board.FindFootprintByReference(ref).FindPadByNumber(str(num)).SetNet(ensure(board, netname))


def pin_num(vc):
    return 48 if vc == 16 else 16 - vc


def main():
    HIST.mkdir(exist_ok=True)
    shutil.copy2(PCB, HIST / "qfbms32_pre_cell_fanout.kicad_pcb")
    board = pcbnew.LoadBoard(str(PCB))
    frozen = {
        fp.GetReference(): (round(mm(fp.GetPosition().x), 4), round(mm(fp.GetPosition().y), 4), round(fp.GetOrientation().AsDegrees(), 3))
        for fp in board.GetFootprints()
    }

    for ref, name in (("U_BQ1", "BQ1_BAT"), ("U_BQ2", "BQ2_BAT")):
        print(ref, "pin47", board.FindFootprintByReference(ref).FindPadByNumber("47").GetNetname(), "->", name)
        setpad(board, ref, 47, name)

    # AGM15T03LL: pad 1 gate, pads 2-8 source, tab drain.
    setpad(board, "Q1", 1, "Q1_GATE")
    setpad(board, "Q1", 4, "CHG+")
    setpad(board, "Q2", 1, "Q2_GATE")
    setpad(board, "Q2", 4, "PACK+")

    world = World()
    for fp in board.GetFootprints():
        for pad in fp.Pads():
            world.add_pad(pad.GetNetname(), pad)
    for t in board.GetTracks():
        layer = 0 if t.GetLayer() == pcbnew.B_Cu else 1
        world.add_seg(t.GetNetname(), layer, mm(t.GetStart().x), mm(t.GetStart().y), mm(t.GetEnd().x), mm(t.GetEnd().y), mm(t.GetWidth()) / 2)

    jobs = []
    for k in range(1, 33):
        rf = board.FindFootprintByReference(f"R_F{k}")
        mon = next(p for p in rf.Pads() if p.GetNumber() == "2")
        cell_n = 33 - k
        chip = "U_BQ1" if cell_n <= 16 else "U_BQ2"
        vc = cell_n if cell_n <= 16 else cell_n - 16
        bq = board.FindFootprintByReference(chip).FindPadByNumber(str(pin_num(vc)))
        if bq.GetNetname() != mon.GetNetname():
            raise RuntimeError(f"{mon.GetNetname()} vs {bq.GetNetname()}")
        caps = [p for ci in range(1, 33) for p in board.FindFootprintByReference(f"C_F{ci}").Pads() if p.GetNetname() == mon.GetNetname()]
        jobs.append((mon.GetNetname(), mon, bq, caps))

    failed = []
    # trunks first so every column is reserved
    for net, mon, bq, caps in jobs:
        sx, sy = mm(mon.GetPosition().x), mm(mon.GetPosition().y)
        put_via(board, world, net, sx, sy)
        put_track(board, world, net, 0, sx, sy, sx, TRUNK_Y)

    order = jobs[15::-1] + jobs[31:15:-1]
    for net, mon, bq, caps in order:
        sx = mm(mon.GetPosition().x)
        block, via_no, home = world.raster(net, sx)
        groups = []
        for pad in caps + [bq]:
            cs = set(cells(pad))
            groups.append(cs)
            for i, j, layer in cs:
                if inside(i, j):
                    block[layer][j * NX + i] = 0
        si, sj = ij(sx, TRUNK_Y)
        starts = [(si, sj, 0)]
        pending = [g for g in groups if g and not (set(starts) & g)]
        segs_all, vias_all = [], []
        bad = False
        guard = 0
        while pending and guard < 6:
            guard += 1
            goal = set().union(*pending)
            got = astar(starts, goal, block, via_no, home)
            if got is None:
                bad = True
                break
            nodes, parent = got
            segs, vias = emit(nodes, parent)
            segs_all.extend(segs)
            vias_all.extend(vias)
            hit = set(nodes)
            pending = [g for g in pending if not (hit & g)]
            starts = list(nodes)
        if bad or pending:
            print("FAIL", net, "left", len(pending))
            failed.append(net)
            continue
        for layer, x1, y1, x2, y2 in segs_all:
            put_track(board, world, net, layer, x1, y1, x2, y2)
        seen = set()
        for x, y in vias_all:
            key = (round(x, 3), round(y, 3))
            if key in seen:
                continue
            seen.add(key)
            put_via(board, world, net, x, y)
        print("OK", net, "vias", len(seen))

    # VC0 cap to the direct pin
    for chip, cell_net in (("U_BQ1", "CELL0"), ("U_BQ2", "CELL16")):
        pin = board.FindFootprintByReference(chip).FindPadByNumber("16")
        caps = [p for ci in range(1, 33) for p in board.FindFootprintByReference(f"C_F{ci}").Pads() if p.GetNetname() == cell_net]
        if not caps:
            print("no cap", cell_net)
            continue
        anchor = caps[0]
        ax, ay = mm(anchor.GetPosition().x), mm(anchor.GetPosition().y)
        block, via_no, home = world.raster(cell_net, ax)
        groups = []
        for pad in caps + [pin]:
            cs = set(cells(pad))
            groups.append(cs)
            for i, j, layer in cs:
                if inside(i, j):
                    block[layer][j * NX + i] = 0
        starts = [(i, j, layer) for i, j, layer in cells(anchor) if inside(i, j)]
        pending = [g for g in groups if g and not (set(starts) & g)]
        segs_all, vias_all, bad = [], [], False
        guard = 0
        while pending and guard < 5:
            guard += 1
            got = astar(starts, set().union(*pending), block, via_no, ax)
            if got is None:
                bad = True
                break
            nodes, parent = got
            segs, vias = emit(nodes, parent)
            segs_all += segs
            vias_all += vias
            hit = set(nodes)
            pending = [g for g in pending if not (hit & g)]
            starts = list(nodes)
        if bad or pending:
            print("FAIL", cell_net)
            failed.append(cell_net)
        else:
            for layer, x1, y1, x2, y2 in segs_all:
                put_track(board, world, cell_net, layer, x1, y1, x2, y2)
            for x, y in vias_all:
                put_via(board, world, cell_net, x, y)
            print("OK", cell_net)

    moved = [ref for ref, pos in frozen.items() if pos != (
        round(mm(board.FindFootprintByReference(ref).GetPosition().x), 4),
        round(mm(board.FindFootprintByReference(ref).GetPosition().y), 4),
        round(board.FindFootprintByReference(ref).GetOrientation().AsDegrees(), 3),
    )]
    if moved:
        raise RuntimeError(moved[:6])
    print("failed", failed)
    if failed:
        print("not saved")
        return
    pcbnew.SaveBoard(str(PCB), board)
    print("saved filter", "vias", sum(1 for t in board.GetTracks() if t.GetClass() == "PCB_VIA"))


if __name__ == "__main__":
    main()
