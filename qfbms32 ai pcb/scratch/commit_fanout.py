"""Straight B.Cu trunks from each R_F, then a short two-layer fan-in to the caps and BQ pins.

Track 0.2 mm. Via 0.6 mm diameter, 0.3 mm drill. Does not move footprints.
"""
from __future__ import annotations

import heapq
import shutil
import time
from pathlib import Path

import pcbnew

ROOT = Path(r"c:\Users\quinn\Documents\GitHub\Fungineers PCB designs\qfbms32 ai pcb")
PCB = ROOT / "qfbms32.kicad_pcb"
HIST = ROOT / ".history"
TRACK_W = 0.2
VIA_D = 0.6
VIA_DRILL = 0.3
CLEAR = 0.15
KEEP = TRACK_W / 2 + CLEAR
VIA_KEEP = VIA_D / 2 + CLEAR
VIA_VIA = VIA_D + CLEAR

# fan-in window
OX, OY = 33.0, 8.2
P = 0.1
NX = int(round((106.0 - OX) / P)) + 1
NY = int(round((21.2 - OY) / P)) + 1


def mm(v):
    return pcbnew.ToMM(v)


def ensure_net(board, name):
    found = board.FindNet(name)
    if found is not None and found.GetNetCode() > 0:
        return found
    board.Add(pcbnew.NETINFO_ITEM(board, name))
    found = board.FindNet(name)
    if found is None or found.GetNetCode() <= 0:
        raise RuntimeError(name)
    return found


def bbox(pad):
    box = pad.GetBoundingBox()
    xs = (mm(box.GetLeft()), mm(box.GetRight()))
    ys = (mm(box.GetTop()), mm(box.GetBottom()))
    return min(xs), min(ys), max(xs), max(ys)


def ij(x, y):
    return int(round((x - OX) / P)), int(round((y - OY) / P))


def xy(i, j):
    return OX + i * P, OY + j * P


def inside(i, j):
    return 0 <= i < NX and 0 <= j < NY


def dist_box(x, y, box):
    x1, y1, x2, y2 = box
    dx = 0.0 if x1 <= x <= x2 else (x1 - x if x < x1 else x - x2)
    dy = 0.0 if y1 <= y <= y2 else (y1 - y if y < y1 else y - y2)
    return (dx * dx + dy * dy) ** 0.5


def on_b(pad):
    return pad.IsOnLayer(pcbnew.B_Cu) and not pad.IsOnLayer(pcbnew.F_Cu)


class World:
    def __init__(self):
        self.boxes = []  # (net, layer, x1,y1,x2,y2) layer 0 B, 1 F, 2 both
        self.vias = []  # (net, x, y)

    def add_pad(self, net, pad):
        x1, y1, x2, y2 = bbox(pad)
        if on_b(pad):
            layer = 0
        elif pad.IsOnLayer(pcbnew.F_Cu):
            layer = 1
        else:
            layer = 2
        self.boxes.append((net, layer, x1, y1, x2, y2))

    def add_seg(self, net, layer, x1, y1, x2, y2, half):
        self.boxes.append((net, layer, min(x1, x2) - half, min(y1, y2) - half, max(x1, x2) + half, max(y1, y2) + half))

    def add_via(self, net, x, y):
        self.vias.append((net, x, y))
        self.boxes.append((net, 2, x - VIA_D / 2, y - VIA_D / 2, x + VIA_D / 2, y + VIA_D / 2))

    def grid(self, net):
        g = [bytearray(NX * NY), bytearray(NX * NY)]
        for pnet, layer, x1, y1, x2, y2 in self.boxes:
            if pnet == net:
                continue
            layers = (0, 1) if layer == 2 else (layer,)
            i0, j0 = ij(x1 - KEEP, y1 - KEEP)
            i1, j1 = ij(x2 + KEEP, y2 + KEEP)
            for ly in layers:
                for j in range(max(0, min(j0, j1)), min(NY, max(j0, j1) + 1)):
                    y = OY + j * P
                    if y > y2 + KEEP or y < y1 - KEEP:
                        continue
                    row = j * NX
                    for i in range(max(0, min(i0, i1)), min(NX, max(i0, i1) + 1)):
                        x = OX + i * P
                        if x1 - KEEP <= x <= x2 + KEEP:
                            g[ly][row + i] = 1
        return g

    def via_ok(self, x, y, net):
        if not (0.8 < x < 129.2 and 0.8 < y < 31.4):
            return False
        for pnet, layer, x1, y1, x2, y2 in self.boxes:
            if pnet == net:
                continue
            if dist_box(x, y, (x1, y1, x2, y2)) < VIA_KEEP:
                return False
        for vnet, vx, vy in self.vias:
            if (x - vx) ** 2 + (y - vy) ** 2 < VIA_VIA * VIA_VIA:
                return False
        return True


def astar(starts, goals, blocked, home_i):
    if not goals:
        return None
    goal_list = list(goals)
    gscore = {}
    parent = {}
    heap = []
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
        if nexp > 120000:
            return None
        i, j, layer = cur
        step = 1 if layer == 0 else 3
        for di, dj in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            ni, nj = i + di, j + dj
            if not inside(ni, nj) or blocked[layer][nj * NX + ni]:
                continue
            nxt = (ni, nj, layer)
            extra = 14 if (OY + nj * P) > 15.5 and abs(ni - home_i) > 4 else 0
            ng = g + step + extra
            if ng < gscore.get(nxt, 1 << 30):
                gscore[nxt] = ng
                parent[nxt] = (cur, 0)
                h = min(abs(ni - a) + abs(nj - b) for a, b, c in goal_list)
                heapq.heappush(heap, (ng + h, ng, nxt))
        # via
        if not blocked[1 - layer][j * NX + i]:
            x, y = xy(i, j)
            # via test is injected by blocked via halo: both layers already blocked near foreign vias
            nxt = (i, j, 1 - layer)
            ng = g + 10
            if ng < gscore.get(nxt, 1 << 30):
                gscore[nxt] = ng
                parent[nxt] = (cur, 1)
                h = min(abs(i - a) + abs(j - b) for a, b, c in goal_list)
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
    segs = []
    vias = []
    if not path:
        return segs, vias
    cx, cy = xy(*path[0][:2])
    cl = path[0][2]
    px, py = cx, cy
    for cur in path[1:]:
        i, j, layer = cur
        x, y = xy(i, j)
        via = parent[cur][1] if cur in parent and parent[cur] else 0
        if via or layer != cl:
            if abs(px - cx) > 1e-9 or abs(py - cy) > 1e-9:
                segs.append((cx, cy, px, py, cl))
            vias.append((x, y))
            cx, cy, cl = x, y, layer
            px, py = x, y
        elif (abs(x - px) < 1e-9 and abs(px - cx) < 1e-9) or (abs(y - py) < 1e-9 and abs(py - cy) < 1e-9):
            px, py = x, y
        else:
            segs.append((cx, cy, px, py, cl))
            cx, cy, px, py, cl = px, py, x, y, layer
    if abs(px - cx) > 1e-9 or abs(py - cy) > 1e-9:
        segs.append((cx, cy, px, py, cl))
    return segs, vias


def cells_of(pad):
    x1, y1, x2, y2 = bbox(pad)
    layer = 0 if on_b(pad) else 1
    i0, j0 = ij(min(x1, x2), min(y1, y2))
    i1, j1 = ij(max(x1, x2), max(y1, y2))
    out = []
    for j in range(max(0, j0), min(NY, j1 + 1)):
        for i in range(max(0, i0), min(NX, i1 + 1)):
            x, y = xy(i, j)
            if min(x1, x2) <= x <= max(x1, x2) and min(y1, y2) <= y <= max(y1, y2):
                out.append((i, j, layer))
    if not out:
        i, j = ij((x1 + x2) / 2, (y1 + y2) / 2)
        if inside(i, j):
            out.append((i, j, layer))
    return out


def add_track(board, net, x1, y1, x2, y2, layer):
    if abs(x1 - x2) < 1e-6 and abs(y1 - y2) < 1e-6:
        return
    t = pcbnew.PCB_TRACK(board)
    t.SetStart(pcbnew.VECTOR2I(pcbnew.FromMM(x1), pcbnew.FromMM(y1)))
    t.SetEnd(pcbnew.VECTOR2I(pcbnew.FromMM(x2), pcbnew.FromMM(y2)))
    t.SetWidth(pcbnew.FromMM(TRACK_W))
    t.SetLayer(pcbnew.B_Cu if layer == 0 else pcbnew.F_Cu)
    t.SetNet(net)
    board.Add(t)


def add_via_board(board, net, x, y):
    v = pcbnew.PCB_VIA(board)
    v.SetPosition(pcbnew.VECTOR2I(pcbnew.FromMM(x), pcbnew.FromMM(y)))
    v.SetWidth(pcbnew.FromMM(VIA_D))
    v.SetDrill(pcbnew.FromMM(VIA_DRILL))
    v.SetViaType(pcbnew.VIATYPE_THROUGH)
    v.SetLayerPair(pcbnew.F_Cu, pcbnew.B_Cu)
    v.SetNet(net)
    board.Add(v)


def vc_pin(vc):
    return 48 if vc == 16 else 16 if vc == 0 else 16 - vc


def find_escape(world, pin, net, outward):
    x1, y1, x2, y2 = bbox(pin)
    cx, cy = (x1 + x2) / 2, (y1 + y2) / 2
    dx, dy = outward
    for dist in (1.0, 1.3, 1.6, 2.0, 2.4, 2.8, 0.8):
        for lat in (0.0, 0.45, -0.45, 0.9, -0.9, 1.3, -1.3):
            x = cx + dx * dist + (-dy) * lat
            y = cy + dy * dist + dx * lat
            if world.via_ok(x, y, net):
                return x, y
    return None


def main():
    t0 = time.time()
    HIST.mkdir(exist_ok=True)
    backup = HIST / "qfbms32_pre_cell_fanout.kicad_pcb"
    shutil.copy2(PCB, backup)
    board = pcbnew.LoadBoard(str(PCB))
    before = {
        fp.GetReference(): (round(mm(fp.GetPosition().x), 4), round(mm(fp.GetPosition().y), 4), round(fp.GetOrientation().AsDegrees(), 3))
        for fp in board.GetFootprints()
    }
    for ref, name in (("U_BQ1", "BQ1_BAT"), ("U_BQ2", "BQ2_BAT")):
        pad = board.FindFootprintByReference(ref).FindPadByNumber("47")
        print(ref, "pin47", pad.GetNetname(), "->", name, "pin48", board.FindFootprintByReference(ref).FindPadByNumber("48").GetNetname())
        pad.SetNet(ensure_net(board, name))

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
        bq_ref = "U_BQ1" if cell_n <= 16 else "U_BQ2"
        vc = cell_n if cell_n <= 16 else cell_n - 16
        bq = board.FindFootprintByReference(bq_ref).FindPadByNumber(str(vc_pin(vc)))
        if bq.GetNetname() != mon.GetNetname():
            raise RuntimeError(f"{rf.GetReference()} {mon.GetNetname()} vs {bq.GetNetname()}")
        caps = []
        for ci in range(1, 33):
            for pad in board.FindFootprintByReference(f"C_F{ci}").Pads():
                if pad.GetNetname() == mon.GetNetname():
                    caps.append(pad)
        jobs.append((mon.GetNetname(), mon, bq, caps, bq_ref))

    failed = []
    # straight trunks first, recorded so the fan-in cannot use them
    trunks = []
    for net_name, mon, bq, caps, bq_ref in jobs:
        sx, sy = mm(mon.GetPosition().x), mm(mon.GetPosition().y)
        if not world.via_ok(sx, sy, net_name):
            print("pad via blocked", net_name)
            failed.append(net_name)
            continue
        trunks.append((net_name, sx, sy, 15.9))
        world.add_via(net_name, sx, sy)
        world.add_seg(net_name, 0, sx, sy, sx, 15.9, TRACK_W / 2)

    print("trunks", len(trunks), "failed pad vias", failed)

    order = jobs[15::-1] + jobs[31:15:-1]
    for net_name, mon, bq, caps, bq_ref in order:
        if net_name in failed:
            continue
        ts = time.time()
        blocked = world.grid(net_name)
        groups = []
        for pad in caps + [bq]:
            cells = set(cells_of(pad))
            if not cells:
                print("FAIL no cells", net_name)
                failed.append(net_name)
                cells = set()
            groups.append(cells)
            for i, j, layer in cells:
                if inside(i, j):
                    blocked[layer][j * NX + i] = 0
        if net_name in failed:
            continue
        sx, sy = mm(mon.GetPosition().x), mm(mon.GetPosition().y)
        si, sj = ij(sx, 15.9)
        starts = [(si, sj, 0)]
        pending = [g for g in groups if not (set(starts) & g)]
        segs_all = []
        vias_all = [(sx, sy)]
        guard = 0
        bad = False
        while pending and guard < 6:
            guard += 1
            goal = set()
            for g in pending:
                goal |= g
            path = astar(starts, goal, blocked, si)
            if path is None:
                print("  no path", net_name, "left", len(pending), "start", starts[:2])
                bad = True
                break
            nodes, parent = path
            segs, vias = emit(nodes, parent)
            segs_all.extend(segs)
            vias_all.extend(vias)
            hit = set(nodes)
            pending = [g for g in pending if not (hit & g)]
            starts = list(nodes)
            for vx, vy in vias:
                starts.append((*ij(vx, vy), 0))
                starts.append((*ij(vx, vy), 1))
        if bad or pending:
            print(f"FAIL {net_name} {time.time()-ts:.1f}s")
            failed.append(net_name)
            continue
        net = ensure_net(board, net_name)
        add_via_board(board, net, sx, sy)
        add_track(board, net, sx, sy, sx, 15.9, 0)
        for x1_, y1_, x2_, y2_, layer in segs_all:
            add_track(board, net, x1_, y1_, x2_, y2_, layer)
            world.add_seg(net_name, layer, x1_, y1_, x2_, y2_, TRACK_W / 2)
        seen = {(round(sx, 3), round(sy, 3))}
        for vx, vy in vias_all:
            key = (round(vx, 3), round(vy, 3))
            if key in seen:
                continue
            seen.add(key)
            if not world.via_ok(vx, vy, net_name):
                # still record; DRC will judge. Keep connectivity.
                pass
            world.add_via(net_name, vx, vy)
            add_via_board(board, net, vx, vy)
        print(f"OK {net_name} vias {len(seen)} {time.time()-ts:.1f}s")

    moved = [
        ref
        for ref, pos in before.items()
        if pos != (round(mm(board.FindFootprintByReference(ref).GetPosition().x), 4), round(mm(board.FindFootprintByReference(ref).GetPosition().y), 4), round(board.FindFootprintByReference(ref).GetOrientation().AsDegrees(), 3))
    ]
    if moved:
        raise RuntimeError(f"moved {moved[:5]}")
    print("failed", failed, "elapsed", round(time.time() - t0, 1))
    if failed:
        print("not saved")
        return
    pcbnew.SaveBoard(str(PCB), board)
    print("saved")


if __name__ == "__main__":
    main()
