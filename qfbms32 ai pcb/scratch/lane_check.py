"""How many F.Cu Y lanes are clear across the filter spans."""
import json

d = json.load(open(r"c:\Users\quinn\Documents\GitHub\Fungineers PCB designs\qfbms32 ai pcb\scratch\filter_geom.json", encoding="utf-8"))

# F.Cu-ish layers from the dump
F_LAYERS = {
    "00000000_00000000_00000000_00002003",
    "00000000_00000000_00000000_00002000",
    "00000000_00000000_00000000_00000003",
    "00000000_00000000_55555555_55555555",
    "00000000_00000000_55555555_5555555f",
    "00000000_00000000_55555555_5555755f",
}
rects = []
for o in d["obstacles"]:
    if o["layer"] in F_LAYERS:
        x1, y1, x2, y2 = o["bb"]
        rects.append((x1, y1, x2, y2, o["ref"]))
for s in d["segs"]:
    if s["layer"] != "F.Cu":
        continue
    w = s["w"] / 2
    x1, x2 = sorted((s["x1"], s["x2"]))
    y1, y2 = sorted((s["y1"], s["y2"]))
    rects.append((x1 - w, y1 - w, x2 + w, y2 + w, "trk:" + s["net"]))

KEEP = 0.25  # track center to copper edge

def blocked_at(y, xa, xb):
    hit = []
    for x1, y1, x2, y2, ref in rects:
        if y2 < y - KEEP or y1 > y + KEEP:
            continue
        if x2 < xa or x1 > xb:
            continue
        hit.append(ref)
    return hit

# full span of both groups
spans = {
    "bq2": (36.5, 69.5),
    "bq1": (68.5, 101.5),
    "all": (36.5, 101.5),
}
print("Y clear across span (no hit):")
for name, (xa, xb) in spans.items():
    clear = []
    y = 15.0
    while y <= 29.8:
        if not blocked_at(y, xa, xb):
            clear.append(round(y, 2))
        y += 0.05
    # compress to ranges
    ranges = []
    if clear:
        start = prev = clear[0]
        for v in clear[1:]:
            if v - prev > 0.06:
                ranges.append((start, prev))
                start = v
            prev = v
        ranges.append((start, prev))
    print(name, "ranges", ranges)

# per-net span: source x to a nominal target x inside the cap field
# BQ2 sources
print("\nper-net clear Y count, pitch 0.4 greedy")
nets = []
for k in range(1, 33):
    rf = d["parts"][f"R_F{k}"]
    p2 = [p for p in rf["pads"] if p["num"] == "2"][0]
    nets.append((p2["net"], p2["x"]))

def greedy(nets, y0, y1):
    used = []  # (y, xa, xb)
    chosen = []
    for net, sx in nets:
        # target roughly the cap field center of its chip
        if net.startswith("BQ2"):
            tx = 44.0
        else:
            tx = 86.0
        xa, xb = (min(sx, tx) - 0.4, max(sx, tx) + 0.4)
        y = y0
        ok = None
        while y <= y1:
            if any(abs(y - uy) < 0.38 and not (xb < uxa or xa > uxb) for uy, uxa, uxb in used):
                y += 0.05
                continue
            if not blocked_at(y, xa, xb):
                ok = y
                break
            y += 0.05
        if ok is None:
            chosen.append((net, None))
        else:
            used.append((ok, xa, xb))
            chosen.append((net, round(ok, 2)))
    return chosen

for label, y0, y1 in (("low", 15.2, 22.5), ("mid", 19.0, 26.2), ("high", 24.0, 29.5), ("wide", 15.2, 29.5)):
    ch = greedy(nets, y0, y1)
    miss = [n for n, y in ch if y is None]
    print(label, "placed", 32 - len(miss), "miss", miss)
