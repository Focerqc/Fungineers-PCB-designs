import json
d = json.load(open(r"c:\Users\quinn\Documents\GitHub\Fungineers PCB designs\qfbms32 ai pcb\scratch\filter_geom.json", encoding="utf-8"))
pts = [(41.43, 26.12), (47.44, 26.12), (69.47, 25.4)]
rects = []
for o in d["obstacles"]:
    if "002003" in o["layer"] or o["layer"].endswith("002000"):
        rects.append((o["ref"], o["num"], o["net"], o["bb"]))
for s in d["segs"]:
    w = s["w"] / 2
    x1, x2 = sorted((s["x1"], s["x2"]))
    y1, y2 = sorted((s["y1"], s["y2"]))
    rects.append((s["net"], "trk", s["net"], (x1 - w, y1 - w, x2 + w, y2 + w)))

def db(x, y, r):
    a, b, c, d = r
    dx = 0 if a <= x <= c else (a - x if x < a else x - c)
    dy = 0 if b <= y <= d else (b - y if y < b else y - d)
    return (dx * dx + dy * dy) ** 0.5

for x, y in pts:
    print("POINT", x, y)
    near = []
    for ref, num, net, r in rects:
        dist = db(x, y, r)
        if dist < 0.6:
            near.append((dist, ref, num, net, tuple(round(v, 2) for v in r)))
    for row in sorted(near)[:8]:
        print(" ", row)
