"""
Route cell-filter path on PCB:
  J_CELL pad (CELL*) -> R_F cell pad
  R_F VC pad -> via near R_F -> B.Cu fan toward C_F / BQ pads

Does not move fixed connectors. Freer via placement OK.
"""
from __future__ import annotations

import shutil
from pathlib import Path

import pcbnew

ROOT = Path(__file__).resolve().parents[1]
PCB = ROOT / "qfbms32.kicad_pcb"
HIST = ROOT / ".history"

TRACK_W = 0.2  # mm
VIA_SIZE = 0.6
VIA_DRILL = 0.3


def net(board: pcbnew.BOARD, name: str) -> pcbnew.NETINFO_ITEM:
    existing = board.FindNet(name)
    if existing and existing.GetNetCode() > 0:
        return existing
    ni = pcbnew.NETINFO_ITEM(board, name)
    board.Add(ni)
    return ni


def add_track(board, x1, y1, x2, y2, netname, width=TRACK_W, layer=pcbnew.F_Cu):
    if abs(x1 - x2) < 1e-6 and abs(y1 - y2) < 1e-6:
        return None
    t = pcbnew.PCB_TRACK(board)
    t.SetStart(pcbnew.VECTOR2I(pcbnew.FromMM(x1), pcbnew.FromMM(y1)))
    t.SetEnd(pcbnew.VECTOR2I(pcbnew.FromMM(x2), pcbnew.FromMM(y2)))
    t.SetWidth(pcbnew.FromMM(width))
    t.SetLayer(layer)
    t.SetNet(net(board, netname))
    board.Add(t)
    return t


def add_via(board, x, y, netname):
    v = pcbnew.PCB_VIA(board)
    v.SetPosition(pcbnew.VECTOR2I(pcbnew.FromMM(x), pcbnew.FromMM(y)))
    v.SetWidth(pcbnew.FromMM(VIA_SIZE))
    v.SetDrill(pcbnew.FromMM(VIA_DRILL))
    v.SetNet(net(board, netname))
    board.Add(v)
    return v


def pad_xy(pad) -> tuple[float, float]:
    p = pad.GetPosition()
    return pcbnew.ToMM(p.x), pcbnew.ToMM(p.y)


def main() -> None:
    HIST.mkdir(exist_ok=True)
    shutil.copy2(PCB, HIST / "qfbms32_pre_route_filters.kicad_pcb")
    board = pcbnew.LoadBoard(str(PCB))

    # Remove prior filter-route tracks/vias tagged by net if re-run? Keep simple: only add if
    # R_F pad has no copper connected yet (track count for that net from this pad ~ 0).
    # For idempotency, skip nets that already have >2 tracks.
    existing_tracks = {}
    for t in board.GetTracks():
        n = t.GetNetname()
        existing_tracks[n] = existing_tracks.get(n, 0) + 1

    routed = 0
    for k in range(1, 33):
        rf = board.FindFootprintByReference(f"R_F{k}")
        if not rf:
            print("missing", f"R_F{k}")
            continue
        cell_n = 33 - k
        cell_net = f"CELL{cell_n}"
        if cell_n <= 16:
            vc_net = f"BQ1_VC{cell_n}"
            bq_ref = "U_BQ1"
        else:
            vc_net = f"BQ2_VC{cell_n - 16}"
            bq_ref = "U_BQ2"

        # Identify R_F pads by net
        cell_pad = vc_pad = None
        for p in rf.Pads():
            if p.GetNetname() == cell_net:
                cell_pad = p
            elif p.GetNetname() == vc_net:
                vc_pad = p
        if not cell_pad or not vc_pad:
            print(f"R_F{k} missing nets cell={cell_net} vc={vc_net}")
            continue

        if existing_tracks.get(cell_net, 0) >= 1 and existing_tracks.get(vc_net, 0) >= 2:
            continue

        # Find matching cell connector pad
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
            print("no connector pad for", cell_net)
            continue

        jx, jy = pad_xy(jpad)
        cx, cy = pad_xy(cell_pad)
        vx, vy = pad_xy(vc_pad)

        # CELL: connector -> R_F (L path on F.Cu)
        add_track(board, jx, jy, jx, cy, cell_net, layer=pcbnew.F_Cu)
        add_track(board, jx, cy, cx, cy, cell_net, layer=pcbnew.F_Cu)

        # VC: R_F -> via just below R_F (board bottom is y~32) or toward BQ (y smaller)
        # R_F at y~30.3, BQ at y~13.8 — via at (vx, 28.5) then B.Cu toward BQ pad
        via_y = 28.5
        add_track(board, vx, vy, vx, via_y, vc_net, layer=pcbnew.F_Cu)
        add_via(board, vx, via_y, vc_net)

        # Find BQ pad for this VC net
        bq = board.FindFootprintByReference(bq_ref)
        bq_pad = None
        for p in bq.Pads():
            if p.GetNetname() == vc_net:
                bq_pad = p
                break
        # CELL0 / CELL16 special: BQ VC0 may be on CELL net directly
        if not bq_pad and cell_n in (0, 16):
            for p in bq.Pads():
                if p.GetNetname() == cell_net:
                    bq_pad = p
                    break
        if bq_pad:
            bx, by = pad_xy(bq_pad)
            # B.Cu: via -> under BQ pad x, then to pad
            add_track(board, vx, via_y, vx, by, vc_net, layer=pcbnew.B_Cu)
            add_track(board, vx, by, bx, by, vc_net, layer=pcbnew.B_Cu)
        else:
            print(f"no BQ pad for {vc_net}")

        # Tie C_F already on B.Cu near BQ — ensure short stub from C_F pad if same net
        # (C_F pads already netted; optional fanout skipped if crowded)

        routed += 1

    # CELL0: connector already netted; ensure BQ1 VC0 (CELL0) via from nearest sense if needed
    # Mid CELL16 -> BQ2 VC0 is direct on pad net; still route connector to any dedicated path

    pcbnew.SaveBoard(str(PCB), board)
    print(f"Routed {routed} filter channels -> {PCB}")


if __name__ == "__main__":
    main()
