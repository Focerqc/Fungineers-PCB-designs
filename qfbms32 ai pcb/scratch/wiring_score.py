"""Classify each footprint: blank, named-only, or copper to another part."""
from __future__ import annotations

import json
from collections import defaultdict

import pcbnew

PCB = r"c:\Users\quinn\Documents\GitHub\Fungineers PCB designs\qfbms32 ai pcb\qfbms32.kicad_pcb"


def is_signal(pad):
    num = pad.GetNumber() or ""
    return num not in ("", "MP") and not num.startswith("TAB")


def main():
    board = pcbnew.LoadBoard(PCB)
    board.BuildConnectivity()
    conn = board.GetConnectivity()
    fps = list(board.GetFootprints())
    index = {}
    for fp in fps:
        for pad in fp.Pads():
            pos = pad.GetPosition()
            index[(pos.x, pos.y)] = (fp.GetReference(), pad.GetNumber() or "")

    def others(pad, ref):
        found = []
        seen = set()
        try:
            items = list(conn.GetConnectedItems(pad))
        except Exception:
            items = []
        for it in items:
            if type(it).__name__ != "PAD":
                continue
            ip = it.GetPosition()
            ident = index.get((ip.x, ip.y))
            if not ident or ident[0] == ref or ident in seen:
                continue
            seen.add(ident)
            found.append(ident)
        return found

    rows = []
    for fp in sorted(fps, key=lambda f: f.GetReference()):
        ref = fp.GetReference()
        sig = [p for p in fp.Pads() if is_signal(p)]
        named = [p for p in sig if p.GetNetname()]
        copper_pads = []
        partners = set()
        for p in sig:
            hit = others(p, ref)
            if hit:
                copper_pads.append(p.GetNumber())
                for h in hit:
                    partners.add(h[0])
        if not named and not copper_pads:
            state = "blank"
        elif copper_pads:
            state = "copper"
        else:
            state = "named"
        rows.append({
            "ref": ref,
            "value": fp.GetValue(),
            "state": state,
            "sig": len(sig),
            "named": len(named),
            "copper_pads": copper_pads,
            "partners": sorted(partners),
        })

    by = defaultdict(list)
    for r in rows:
        by[r["state"]].append(r)
    print(f"footprints {len(rows)}")
    for st in ("copper", "named", "blank"):
        print(f"\n== {st} {len(by[st])} ==")
        for r in by[st]:
            extra = ""
            if r["partners"]:
                extra = " -> " + ",".join(r["partners"])
            elif r["state"] == "named":
                extra = f" ({r['named']}/{r['sig']} pads named)"
            print(f"  {r['ref']:10} {r['value']:16}{extra}")

    # signal pads
    total = named_n = copper_n = blank_n = 0
    for fp in fps:
        ref = fp.GetReference()
        for p in fp.Pads():
            if not is_signal(p):
                continue
            total += 1
            if others(p, ref):
                copper_n += 1
            elif p.GetNetname():
                named_n += 1
            else:
                blank_n += 1
    print(f"\nSIGNAL PADS {total} copper={copper_n} named_only={named_n} blank={blank_n}")
    print("@@JSON@@")
    print(json.dumps({"counts": {k: len(by[k]) for k in by}, "pads": {"total": total, "copper": copper_n, "named": named_n, "blank": blank_n}}))


if __name__ == "__main__":
    main()
