"""F.Cu vertical clearance at each filter source X."""
import json

d = json.load(open(r"c:\Users\quinn\Documents\GitHub\Fungineers PCB designs\qfbms32 ai pcb\scratch\filter_geom.json", encoding="utf-8"))
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
        rects.append((x1, y1, x2, y2))
for s in d["segs"]:
    if s["layer"] != "F.Cu":
        continue
    w = s["w"] / 2
    x1, x2 = sorted((s["x1"], s["x2"]))
    y1, y2 = sorted((s["y1"], s["y2"]))
    rects.append((x1 - w, y1 - w, x2 + w, y2 + w))

KEEP = 0.25  # centerline to copper

def clear_ys(x, y0=14.5, y1=30.2, step=0.05):
    bad = []
    y = y0
    spans = []
    run = None
    while y <= y1:
        hit = False
        for a, b, c, d in rects:
            if c < x - KEEP or a > x + KEEP:
                continue
            if d < y - KEEP or b > y + KEEP:
                continue
            hit = True
            break
        if not hit:
            if run is None:
                run = y
        else:
            if run is not None:
                spans.append((round(run, 2), round(y - step, 2)))
                run = None
        y += step
    if run is not None:
        spans.append((round(run, 2), round(y1, 2)))
    return spans

print("SOURCE vertical clear spans")
for k in range(1, 33):
    rf = d["parts"][f"R_F{k}"]
    p2 = [p for p in rf["pads"] if p["num"] == "2"][0]
    spans = clear_ys(p2["x"])
    # longest
    longest = max(spans, key=lambda s: s[1] - s[0]) if spans else None
    print(f"R_F{k:02d} {p2['net']:10} x={p2['x']:.2f} longest={longest} n={len(spans)}")
