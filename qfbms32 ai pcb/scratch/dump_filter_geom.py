"""Dump cell-filter geometry for fanout. Read-only."""
from __future__ import annotations

import json
from pathlib import Path

import pcbnew

PCB = Path(r"c:\Users\quinn\Documents\GitHub\Fungineers PCB designs\qfbms32 ai pcb\qfbms32.kicad_pcb")
OUT = Path(r"c:\Users\quinn\Documents\GitHub\Fungineers PCB designs\qfbms32 ai pcb\scratch\filter_geom.json")


def mm(v) -> float:
    return round(pcbnew.ToMM(v), 4)


def pad_info(pad) -> dict:
    pos = pad.GetPosition()
    size = pad.GetSize()
    bb = pad.GetBoundingBox()
    return {
        "num": pad.GetNumber(),
        "net": pad.GetNetname(),
        "x": mm(pos.x),
        "y": mm(pos.y),
        "sx": mm(size.x),
        "sy": mm(size.y),
        "layer": pad.GetLayerSet().FmtHex() if hasattr(pad.GetLayerSet(), "FmtHex") else str(pad.GetLayer()),
        "attr": pad.GetAttribute(),
        "drill": mm(pad.GetDrillSizeX()) if pad.GetDrillSizeX() else 0,
        "bb": [mm(bb.GetLeft()), mm(bb.GetTop()), mm(bb.GetRight()), mm(bb.GetBottom())],
    }


def main() -> None:
    board = pcbnew.LoadBoard(str(PCB))
    ds = board.GetDesignSettings()
    rules = {
        "min_clearance": mm(ds.m_MinClearance),
        "min_track": mm(ds.m_TrackMinWidth),
        "min_via_dia": mm(ds.m_ViasMinSize),
        "min_via_drill": mm(getattr(ds, "m_MinThroughDrill", 0)),
        "netclass": ds.GetCurrentNetClassName(),
    }
    for name in ("GetNetClasses", "m_NetSettings"):
        pass
    try:
        classes = ds.m_NetSettings.GetNetclasses()
        for name in classes:
            nc = classes[name]
            rules[f"nc_{name}"] = {
                "clearance": mm(nc.GetClearance()),
                "track": mm(nc.GetTrackWidth()),
                "via_d": mm(nc.GetViaDiameter()),
                "via_drill": mm(nc.GetViaDrill()),
            }
    except Exception as exc:
        rules["netclass_err"] = str(exc)
    print("RULES", json.dumps(rules))

    tracks = []
    widths = {}
    layers = {}
    for t in board.GetTracks():
        kind = t.GetClass()
        if kind == "PCB_VIA":
            tracks.append({"kind": "via", "net": t.GetNetname(), "x": mm(t.GetPosition().x), "y": mm(t.GetPosition().y)})
        else:
            w = mm(t.GetWidth())
            widths[w] = widths.get(w, 0) + 1
            lay = t.GetLayerName() if hasattr(t, "GetLayerName") else str(t.GetLayer())
            layers[lay] = layers.get(lay, 0) + 1
    print("TRACK_WIDTHS", widths)
    print("TRACK_LAYERS", layers)
    print("VIAS", sum(1 for t in tracks if t["kind"] == "via"), "TRACKS", sum(widths.values()))

    outline = []
    for d in board.GetDrawings():
        if d.GetLayerName() == "Edge.Cuts" if hasattr(d, "GetLayerName") else False:
            outline.append(d.GetClass())
    # bbox of board
    bb = board.GetBoardEdgesBoundingBox()
    print("BOARD_BB", mm(bb.GetLeft()), mm(bb.GetTop()), mm(bb.GetRight()), mm(bb.GetBottom()))

    want_prefix = ("R_F", "C_F", "R_B", "U_BQ", "J_CELL", "J_T", "D_PRI", "D_SEC")
    parts = {}
    obstacles = []
    for fp in board.GetFootprints():
        ref = fp.GetReference()
        pos = fp.GetPosition()
        entry = {
            "ref": ref,
            "value": fp.GetValue(),
            "x": mm(pos.x),
            "y": mm(pos.y),
            "rot": round(fp.GetOrientation().AsDegrees(), 2),
            "layer": fp.GetLayerName(),
            "pads": [pad_info(p) for p in fp.Pads()],
        }
        if ref.startswith(want_prefix) or ref in ("U_BQ1", "U_BQ2"):
            parts[ref] = entry
        for p in entry["pads"]:
            obstacles.append({
                "ref": ref,
                "num": p["num"],
                "net": p["net"],
                "bb": p["bb"],
                "layer": p["layer"],
                "attr": p["attr"],
                "drill": p["drill"],
                "x": p["x"],
                "y": p["y"],
            })

    # existing track segments, compressed
    segs = []
    for t in board.GetTracks():
        if t.GetClass() == "PCB_VIA":
            continue
        segs.append({
            "net": t.GetNetname(),
            "layer": t.GetLayerName() if hasattr(t, "GetLayerName") else str(t.GetLayer()),
            "w": mm(t.GetWidth()),
            "x1": mm(t.GetStart().x),
            "y1": mm(t.GetStart().y),
            "x2": mm(t.GetEnd().x),
            "y2": mm(t.GetEnd().y),
        })

    payload = {"rules": rules, "parts": parts, "obstacles": obstacles, "segs": segs}
    OUT.write_text(json.dumps(payload), encoding="utf-8")
    print("WROTE", OUT, "parts", len(parts), "obs", len(obstacles), "segs", len(segs))

    # concise filter map
    for k in range(1, 33):
        rf = parts[f"R_F{k}"]
        pads = ", ".join(f"p{p['num']} {p['net']} ({p['x']:.3f},{p['y']:.3f}) {p['sx']:.2f}x{p['sy']:.2f} L{p['layer']}" for p in rf["pads"])
        print(f"R_F{k} rot={rf['rot']} {pads}")
    for k in (1, 8, 9, 16, 17, 24, 25, 32):
        cf = parts[f"C_F{k}"]
        pads = ", ".join(f"p{p['num']} {p['net']} ({p['x']:.3f},{p['y']:.3f}) {p['sx']:.2f}x{p['sy']:.2f}" for p in cf["pads"])
        print(f"C_F{k} layer={cf['layer']} rot={cf['rot']} @({cf['x']:.3f},{cf['y']:.3f}) {pads}")
    for ref in ("U_BQ1", "U_BQ2"):
        bq = parts[ref]
        print(ref, "rot", bq["rot"], "at", bq["x"], bq["y"], "layer", bq["layer"])
        for p in bq["pads"]:
            if p["num"] in {str(i) for i in list(range(1, 17)) + [47, 48]} or p["net"].startswith("BQ") or p["net"].startswith("CELL"):
                print(f"  pin {p['num']} {p['net']} ({p['x']:.3f},{p['y']:.3f}) {p['sx']:.3f}x{p['sy']:.3f}")


if __name__ == "__main__":
    main()
