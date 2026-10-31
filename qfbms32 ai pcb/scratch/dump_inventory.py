"""Dump footprint positions, values, pad nets, and track counts."""
from __future__ import annotations

import pcbnew

PCB = r"c:\Users\quinn\Documents\GitHub\Fungineers PCB designs\qfbms32 ai pcb\qfbms32.kicad_pcb"


def mm(v):
    return round(pcbnew.ToMM(v), 3)


def main():
    board = pcbnew.LoadBoard(PCB)
    fps = sorted(board.GetFootprints(), key=lambda f: (f.GetReference()[:1], f.GetReference()))
    # natural-ish: print grouped
    print("=== FOOTPRINTS ===")
    for fp in sorted(board.GetFootprints(), key=lambda f: f.GetReference()):
        pos = fp.GetPosition()
        pads = []
        for p in fp.Pads():
            num = p.GetNumber() or ""
            if num in ("",) or num.startswith("MP"):
                continue
            pp = p.GetPosition()
            pads.append(f"{num}:{p.GetNetname() or '-'}@{mm(pp.x)},{mm(pp.y)}")
        print(
            f"{fp.GetReference():10} {fp.GetValue():18} "
            f"xy={mm(pos.x):8},{mm(pos.y):7} rot={fp.GetOrientationDegrees():6} "
            f"layer={'B' if fp.GetLayer()==pcbnew.B_Cu else 'F'} "
            f"fp={fp.GetFPIDAsString()} | " + " ".join(pads)
        )
    n_trk = n_via = 0
    by_net = {}
    for t in board.GetTracks():
        if t.GetClass() == "PCB_VIA":
            n_via += 1
        else:
            n_trk += 1
            by_net[t.GetNetname()] = by_net.get(t.GetNetname(), 0) + 1
    print(f"\n=== TRACKS {n_trk} VIAS {n_via} ===")
    for n, c in sorted(by_net.items(), key=lambda kv: -kv[1])[:80]:
        print(f"  {c:4} {n}")
    print("\n=== ZONES ===")
    for z in board.Zones():
        print(f"  {z.GetNetname()} layer={z.GetLayerName()} pri={z.GetAssignedPriority()}")


if __name__ == "__main__":
    main()
