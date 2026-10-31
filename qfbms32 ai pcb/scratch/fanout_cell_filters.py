"""Cell-filter fanout on qfbms32.

Does not move footprints. Track 0.2 mm. Via drill 0.3 mm, diameter 0.6 mm.
Splits U_BQ1/U_BQ2 pin 47 onto BQ1_BAT / BQ2_BAT, then routes each R_F
monitor pad to its C_F pads and the matching BQ VC pin on B.Cu.
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
HALF = TRACK_W / 2
TRACK_KEEP = HALF + CLEAR  # 0.25, track center to foreign copper edge
VIA_KEEP = VIA_D / 2 + CLEAR  # 0.45, via center to foreign copper edge
VIA_VIA = VIA_D + CLEAR  # 0.75, via center to via center

OX, OY = 33.0, 8.0
P = 0.1
NX = int(round((106.0 - OX) / P)) + 1
NY = int(round((31.6 - OY) / P)) + 1
B = 0
F = 1
F_COST = 3
B_COST = 1
VIA_COST = 16
CAP_Y = 15.0  # prefer trunks on the cell side of this


def mm(v) -> float:
    return pcbnew.ToMM(v)


def ensure_net(board, name):
    existing = board.FindNet(name)
    if existing is not None and existing.GetNetCode() > 0:
        return existing
    item = pcbnew.NETINFO_ITEM(board, name)
    board.Add(item)
    found = board.FindNet(name)
    if found is None or found.GetNetCode() <= 0:
        raise RuntimeError(f"could not add net {name}")
    return found


def bbox(pad):
    box = pad.GetBoundingBox()
    xs = (mm(box.GetLeft()), mm(box.GetRight()))
    ys = (mm(box.GetTop()), mm(box.GetBottom()))
    return min(xs), min(ys), max(xs), max(ys)


def inb(i, j) -> bool:
    return 0 <= i < NX and 0 <= j < NY


def ij_of(x, y):
    return int(round((x - OX) / P)), int(round((y - OY) / P))


def xy_of(i, j):
    return OX + i * P, OY + j * P


def node(i, j, layer) -> int:
    return (layer * NY + j) * NX + i


def dec(n):
    i = n % NX
    t = n // NX
    j = t % NY
    layer = t // NY
    return i, j, layer


class Maze:
    def __init__(self):
        self.pads = []  # (net, x1,y1,x2,y2, layer)
        self.segs = []  # (net, x1,y1,x2,y2, half_w, layer)
        self.vias = []  # (net, x, y)

    def add_pad(self, net, pad):
        x1, y1, x2, y2 = bbox(pad)
        if pad.IsOnLayer(pcbnew.B_Cu) and not pad.IsOnLayer(pcbnew.F_Cu):
            layer = B
        elif pad.IsOnLayer(pcbnew.F_Cu) and not pad.IsOnLayer(pcbnew.B_Cu):
            layer = F
        else:
            layer = 2  # both
        self.pads.append((net, x1, y1, x2, y2, layer))

    def add_seg(self, net, x1, y1, x2, y2, half_w, layer):
        self.segs.append((net, x1, y1, x2, y2, half_w, layer))

    def add_via(self, net, x, y):
        self.vias.append((net, x, y))

    def _mark_rect(self, grid, x1, y1, x2, y2):
        i0, j0 = ij_of(x1, y1)
        i1, j1 = ij_of(x2, y2)
        if i0 > i1:
            i0, i1 = i1, i0
        if j0 > j1:
            j0, j1 = j1, j0
        i0 = max(0, i0)
        j0 = max(0, j0)
        i1 = min(NX - 1, i1)
        j1 = min(NY - 1, j1)
        for j in range(j0, j1 + 1):
            base = j * NX
            for i in range(i0, i1 + 1):
                grid[base + i] = 1

    def track_block(self, net):
        """Cells a track center of `net` may not use, per layer."""
        grids = [bytearray(NX * NY), bytearray(NX * NY)]
        for pnet, x1, y1, x2, y2, layer in self.pads:
            if pnet == net:
                continue
            layers = (B, F) if layer == 2 else (layer,)
            for ly in layers:
                self._mark_rect(grids[ly], x1 - TRACK_KEEP, y1 - TRACK_KEEP, x2 + TRACK_KEEP, y2 + TRACK_KEEP)
        for snet, x1, y1, x2, y2, half_w, layer in self.segs:
            if snet == net:
                continue
            keep = half_w + TRACK_KEEP
            self._mark_rect(grids[layer], min(x1, x2) - keep, min(y1, y2) - keep, max(x1, x2) + keep, max(y1, y2) + keep)
        for vnet, x, y in self.vias:
            if vnet == net:
                continue
            self._mark_rect(grids[B], x - VIA_KEEP, y - VIA_KEEP, x + VIA_KEEP, y + VIA_KEEP)
            self._mark_rect(grids[F], x - VIA_KEEP, y - VIA_KEEP, x + VIA_KEEP, y + VIA_KEEP)
        return grids

    def via_grid(self, net, extra):
        """1 = via center not allowed."""
        grid = bytearray(NX * NY)
        # board edge
        for j in range(NY):
            y = OY + j * P
            row = j * NX
            for i in range(NX):
                x = OX + i * P
                if x < 0.8 or x > 129.2 or y < 0.8 or y > 31.3:
                    grid[row + i] = 1
        for pnet, x1, y1, x2, y2, layer in self.pads:
            if pnet == net:
                continue
            self._mark_rect(grid, x1 - VIA_KEEP, y1 - VIA_KEEP, x2 + VIA_KEEP, y2 + VIA_KEEP)
        for snet, x1, y1, x2, y2, half_w, layer in self.segs:
            if snet == net:
                continue
            keep = half_w + VIA_D / 2 + CLEAR
            self._mark_rect(grid, min(x1, x2) - keep, min(y1, y2) - keep, max(x1, x2) + keep, max(y1, y2) + keep)
        for vnet, x, y in self.vias:
            self._mark_rect(grid, x - VIA_VIA, y - VIA_VIA, x + VIA_VIA, y + VIA_VIA)
        for x, y in extra:
            self._mark_rect(grid, x - VIA_VIA, y - VIA_VIA, x + VIA_VIA, y + VIA_VIA)
        return grid


def cells_in(x1, y1, x2, y2):
    i0, j0 = ij_of(min(x1, x2), min(y1, y2))
    i1, j1 = ij_of(max(x1, x2), max(y1, y2))
    out = []
    for j in range(max(0, j0), min(NY, j1 + 1)):
        for i in range(max(0, i0), min(NX, i1 + 1)):
            x, y = xy_of(i, j)
            if min(x1, x2) - 1e-6 <= x <= max(x1, x2) + 1e-6 and min(y1, y2) - 1e-6 <= y <= max(y1, y2) + 1e-6:
                out.append((i, j))
    if not out:
        i, j = ij_of((x1 + x2) / 2, (y1 + y2) / 2)
        if inb(i, j):
            out.append((i, j))
    return out


def astar(starts, goals, blocked, via_fn, near_goal):
    if not goals:
        return None
    goal_list = list(goals)
    gscore = {}
    parent = {}
    via_step = {}
    heap = []
    for s in starts:
        if s in gscore:
            continue
        gscore[s] = 0
        parent[s] = None
        via_step[s] = 0
        heapq.heappush(heap, (0, 0, s))
    best = None
    expanded = 0
    while heap:
        f, g, cur = heapq.heappop(heap)
        if g != gscore.get(cur):
            continue
        if cur in goals:
            best = cur
            break
        expanded += 1
        if expanded > 250000:
            return None
        i, j, layer = cur
        for di, dj in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            ni, nj = i + di, j + dj
            if not inb(ni, nj):
                continue
            if blocked[layer][nj * NX + ni]:
                continue
            nxt = (ni, nj, layer)
            step = B_COST if layer == B else F_COST
            y = OY + nj * P
            if y < CAP_Y and (nj * NX + ni) not in near_goal:
                step += 5
            ng = g + step
            if ng < gscore.get(nxt, 1 << 30):
                gscore[nxt] = ng
                parent[nxt] = cur
                via_step[nxt] = 0
                h = min(abs(ni - gi) + abs(nj - gj) for gi, gj, gl in goal_list)
                heapq.heappush(heap, (ng + h, ng, nxt))
        if via_fn(i, j):
            ol = F if layer == B else B
            if not blocked[ol][j * NX + i]:
                nxt = (i, j, ol)
                ng = g + VIA_COST
                if ng < gscore.get(nxt, 1 << 30):
                    gscore[nxt] = ng
                    parent[nxt] = cur
                    via_step[nxt] = 1
                    h = min(abs(i - gi) + abs(j - gj) for gi, gj, gl in goal_list)
                    heapq.heappush(heap, (ng + h, ng, nxt))
    if best is None:
        return None
    path = []
    cur = best
    while cur is not None:
        path.append((cur, via_step.get(cur, 0)))
        cur = parent[cur]
    path.reverse()
    return path


def compress(path):
    """Return segments (x1,y1,x2,y2,layer) and via points (x,y)."""
    if not path:
        return [], []
    segs = []
    vias = []
    cx, cy = xy_of(path[0][0][0], path[0][0][1])
    cl = path[0][0][2]
    px, py = cx, cy
    for (i, j, layer), is_via in path[1:]:
        x, y = xy_of(i, j)
        if is_via or layer != cl:
            if abs(px - cx) > 1e-9 or abs(py - cy) > 1e-9:
                segs.append((cx, cy, px, py, cl))
            vias.append((x, y))
            cx, cy, cl = x, y, layer
            px, py = x, y
        else:
            # continue if collinear with running segment
            if (abs(x - px) < 1e-9 and abs(px - cx) < 1e-9) or (abs(y - py) < 1e-9 and abs(py - cy) < 1e-9):
                px, py = x, y
            else:
                segs.append((cx, cy, px, py, cl))
                cx, cy = px, py
                px, py = x, y
                cl = layer
    if abs(px - cx) > 1e-9 or abs(py - cy) > 1e-9:
        segs.append((cx, cy, px, py, cl))
    # unique vias
    uniq = []
    seen = set()
    for x, y in vias:
        key = (round(x, 3), round(y, 3))
        if key not in seen:
            seen.add(key)
            uniq.append((x, y))
    return segs, uniq


def add_track(board, net, x1, y1, x2, y2, layer):
    if abs(x1 - x2) < 1e-6 and abs(y1 - y2) < 1e-6:
        return
    t = pcbnew.PCB_TRACK(board)
    t.SetStart(pcbnew.VECTOR2I(pcbnew.FromMM(x1), pcbnew.FromMM(y1)))
    t.SetEnd(pcbnew.VECTOR2I(pcbnew.FromMM(x2), pcbnew.FromMM(y2)))
    t.SetWidth(pcbnew.FromMM(TRACK_W))
    t.SetLayer(pcbnew.B_Cu if layer == B else pcbnew.F_Cu)
    t.SetNet(net)
    board.Add(t)


def add_via(board, net, x, y):
    v = pcbnew.PCB_VIA(board)
    v.SetPosition(pcbnew.VECTOR2I(pcbnew.FromMM(x), pcbnew.FromMM(y)))
    v.SetWidth(pcbnew.FromMM(VIA_D))
    v.SetDrill(pcbnew.FromMM(VIA_DRILL))
    v.SetViaType(pcbnew.VIATYPE_THROUGH)
    v.SetLayerPair(pcbnew.F_Cu, pcbnew.B_Cu)
    v.SetNet(net)
    board.Add(v)


def pad_layer(pad) -> int:
    b = pad.IsOnLayer(pcbnew.B_Cu)
    f = pad.IsOnLayer(pcbnew.F_Cu)
    if b and not f:
        return B
    return F


def main():
    t0 = time.time()
    HIST.mkdir(exist_ok=True)
    backup = HIST / "qfbms32_pre_cell_fanout.kicad_pcb"
    shutil.copy2(PCB, backup)
    print("backup", backup)

    board = pcbnew.LoadBoard(str(PCB))
    before = {
        fp.GetReference(): (round(mm(fp.GetPosition().x), 4), round(mm(fp.GetPosition().y), 4), round(fp.GetOrientation().AsDegrees(), 3))
        for fp in board.GetFootprints()
    }

    zones = list(board.Zones()) if hasattr(board, "Zones") else []
    print("zones", len(zones))

    for ref, name in (("U_BQ1", "BQ1_BAT"), ("U_BQ2", "BQ2_BAT")):
        pad = board.FindFootprintByReference(ref).FindPadByNumber("47")
        old = pad.GetNetname()
        pad.SetNet(ensure_net(board, name))
        pin48 = board.FindFootprintByReference(ref).FindPadByNumber("48").GetNetname()
        print(f"{ref} pin47 {old} -> {pad.GetNetname()}  pin48 {pin48}")

    maze = Maze()
    for fp in board.GetFootprints():
        for pad in fp.Pads():
            maze.add_pad(pad.GetNetname(), pad)
    for t in board.GetTracks():
        if t.GetClass() == "PCB_VIA":
            maze.add_via(t.GetNetname(), mm(t.GetPosition().x), mm(t.GetPosition().y))
        else:
            layer = B if t.GetLayer() == pcbnew.B_Cu else F
            maze.add_seg(
                t.GetNetname(),
                mm(t.GetStart().x), mm(t.GetStart().y),
                mm(t.GetEnd().x), mm(t.GetEnd().y),
                mm(t.GetWidth()) / 2,
                layer,
            )
    print(f"existing pads {len(maze.pads)} segs {len(maze.segs)} vias {len(maze.vias)}")

    def bq_pin(ref, number):
        return board.FindFootprintByReference(ref).FindPadByNumber(str(number))

    def vc_pin_number(vc: int) -> int:
        if vc == 16:
            return 48
        if vc == 0:
            return 16
        return 16 - vc

    jobs = []
    for k in range(1, 33):
        rf = board.FindFootprintByReference(f"R_F{k}")
        mon = None
        for pad in rf.Pads():
            if pad.GetNumber() == "2":
                mon = pad
        net_name = mon.GetNetname()
        cell_n = 33 - k
        if cell_n <= 16:
            bq_ref = "U_BQ1"
            vc = cell_n
        else:
            bq_ref = "U_BQ2"
            vc = cell_n - 16
        bq = bq_pin(bq_ref, vc_pin_number(vc))
        if bq.GetNetname() != net_name:
            raise RuntimeError(f"R_F{k} pad2 {net_name} != {bq_ref} pin {bq.GetNumber()} {bq.GetNetname()}")
        caps = []
        for ci in range(1, 33):
            cf = board.FindFootprintByReference(f"C_F{ci}")
            for pad in cf.Pads():
                if pad.GetNetname() == net_name:
                    caps.append(pad)
        jobs.append((net_name, mon, bq, caps))

    # VC0 caps: direct ties already named CELL0 / CELL16. Connect the cap pad to the BQ pin.
    extras = []
    for ref, num, cell_net in (("U_BQ1", 16, "CELL0"), ("U_BQ2", 16, "CELL16")):
        pin = bq_pin(ref, num)
        if pin.GetNetname() != cell_net:
            raise RuntimeError(f"{ref} pin16 is {pin.GetNetname()}")
        caps = []
        for ci in range(1, 33):
            cf = board.FindFootprintByReference(f"C_F{ci}")
            for pad in cf.Pads():
                if pad.GetNetname() == cell_net:
                    caps.append(pad)
        jack = None
        for cref in ("J_CELL1", "J_CELL2", "J_CELL3", "J_CELL4"):
            fp = board.FindFootprintByReference(cref)
            for pad in fp.Pads():
                if pad.GetNetname() == cell_net and pad.GetNumber().isdigit():
                    jack = pad
        extras.append((cell_net, pin, caps, jack))

    routed = []
    failed = []

    def pad_cells(pad):
        layer = pad_layer(pad)
        x1, y1, x2, y2 = bbox(pad)
        return {(i, j, layer) for i, j in cells_in(x1, y1, x2, y2) if inb(i, j)}

    def run_job(net_name, anchor_pad, targets, pad_via=False):
        grids = maze.track_block(net_name)
        groups = []
        near = set()
        for pad in targets:
            cells = pad_cells(pad)
            if not cells:
                print("  no cells", net_name)
                return False
            groups.append(cells)
            for i, j, layer in cells:
                grids[layer][j * NX + i] = 0
                for dj in range(-12, 13):
                    for di in range(-12, 13):
                        if di * di + dj * dj <= 144 and inb(i + di, j + dj):
                            near.add((j + dj) * NX + (i + di))
        ax, ay = mm(anchor_pad.GetPosition().x), mm(anchor_pad.GetPosition().y)
        path_vias = []
        if pad_via:
            vgrid = maze.via_grid(net_name, [])
            si, sj = ij_of(ax, ay)
            if not inb(si, sj) or vgrid[sj * NX + si]:
                print("  via on pad not clear", net_name, round(ax, 3), round(ay, 3))
                return False
            grids[B][sj * NX + si] = 0
            grids[F][sj * NX + si] = 0
            starts = [(si, sj, B), (si, sj, F)]
            path_vias.append((xy_of(si, sj)))
        else:
            starts = list(pad_cells(anchor_pad))
        # anchor pad is already satisfied
        pending = [g for g in groups if not (set(starts) & g)]
        all_segs = []
        guard = 0
        while pending and guard < 8:
            guard += 1
            goals = set()
            for g in pending:
                goals |= g
            vgrid = maze.via_grid(net_name, path_vias)

            def via_fn(i, j, _vg=vgrid):
                return _vg[j * NX + i] == 0

            path = astar(starts, goals, grids, via_fn, near)
            if path is None:
                return False
            segs, vias = compress(path)
            all_segs.extend(segs)
            path_vias.extend(vias)
            hit = {(i, j, layer) for (i, j, layer), _ in path}
            pending = [g for g in pending if not (hit & g)]
            starts = []
            for (i, j, layer), is_via in path:
                starts.append((i, j, layer))
                if is_via:
                    starts.append((i, j, F if layer == B else B))
        if pending:
            return False
        net = ensure_net(board, net_name)
        for x1, y1, x2, y2, layer in all_segs:
            add_track(board, net, x1, y1, x2, y2, layer)
            maze.add_seg(net_name, x1, y1, x2, y2, HALF, layer)
        seen = set()
        for x, y in path_vias:
            key = (round(x, 3), round(y, 3))
            if key in seen:
                continue
            seen.add(key)
            add_via(board, net, x, y)
            maze.add_via(net_name, x, y)
        return True

    for net_name, mon, bq, caps in jobs:
        ts = time.time()
        print(f"route {net_name} ...", flush=True)
        ok = run_job(net_name, mon, [bq, *caps], pad_via=True)
        print(f"{'OK' if ok else 'FAIL'} {net_name} targets {1+len(caps)} {time.time()-ts:.1f}s")
        (routed if ok else failed).append(net_name)

    for cell_net, pin, caps, jack in extras:
        ts = time.time()
        targets = [pin, *caps]
        if jack is not None:
            targets.append(jack)
        # start at the cap pad (B.Cu); no resistor via
        ok = run_job(cell_net, caps[0], targets)
        print(f"{'OK' if ok else 'FAIL'} {cell_net} vc0 {time.time()-ts:.1f}s")
        (routed if ok else failed).append(cell_net)

    after = {
        fp.GetReference(): (round(mm(fp.GetPosition().x), 4), round(mm(fp.GetPosition().y), 4), round(fp.GetOrientation().AsDegrees(), 3))
        for fp in board.GetFootprints()
    }
    moved = [ref for ref in before if before[ref] != after.get(ref)]
    if moved:
        raise RuntimeError(f"footprints moved: {moved[:8]}")

    n_via = sum(1 for t in board.GetTracks() if t.GetClass() == "PCB_VIA")
    print("failed", failed)
    print("vias", n_via, "drill", VIA_DRILL, "dia", VIA_D, "track", TRACK_W)
    print(f"elapsed {time.time()-t0:.1f}s")
    if failed:
        print("not saved; backup left at", backup)
        return
    pcbnew.SaveBoard(str(PCB), board)
    print("saved", PCB)


if __name__ == "__main__":
    main()
