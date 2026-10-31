"""Which (x, y) can hold a 0.6 mm via without touching existing copper."""
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
B_LAYERS = {
    "00000000_00000000_00000000_0000800c",
    "00000000_00000000_00000000_00000004",
}
f_rects = []
b_rects = []
for o in d["obstacles"]:
    box = o["bb"]
    if o["layer"] in F_LAYERS:
        f_rects.append(box)
    elif o["layer"] in B_LAYERS:
        b_rects.append(box)
for s in d["segs"]:
    w = s["w"] / 2
    x1, x2 = sorted((s["x1"], s["x2"]))
    y1, y2 = sorted((s["y1"], s["y2"]))
    f_rects.append((x1 - w, y1 - w, x2 + w, y2 + w))

KEEP = 0.45

def hits(rects, x, y):
    for x1, y1, x2, y2 in rects:
        dx = 0.0 if x1 <= x <= x2 else min(abs(x - x1), abs(x - x2))
        dy = 0.0 if y1 <= y <= y2 else min(abs(y - y1), abs(y - y2))
        # outside: distance
        if x < x1:
            dx = x1 - x
        elif x > x2:
            dx = x - x2
        else:
            dx = 0.0
        if y < y1:
            dy = y1 - y
        elif y > y2:
            dy = y - y2
        else:
            dy = 0.0
        if dx * dx + dy * dy < KEEP * KEEP:
            return True
    return False

srcs = []
for k in range(1, 33):
    p2 = [p for p in d["parts"][f"R_F{k}"]["pads"] if p["num"] == "2"][0]
    srcs.append((p2["net"], p2["x"]))

print("via-clear Y at source x, and at x-0.85, from 15.5 to 26.2")
for net, x in srcs:
    row = []
    y = 15.6
    while y <= 26.2:
        ok = []
        for dx in (0.0, -0.85, 0.85, -1.3, 1.3):
            if not hits(f_rects, x + dx, y) and not hits(b_rects, x + dx, y):
                ok.append(dx)
                break
        row.append("." if ok else "X")
        y += 0.4
    print(f"{net:10} {x:6.2f} {''.join(row)}")
print("y starts 15.6 step 0.4, '.' means some dx in {0,±0.85,±1.3} is clear")
print("\nY where every net in the group has a via site")
groups = {"BQ2": srcs[:16], "BQ1": srcs[16:]}
y = 15.6
idx = 0
while y <= 26.2:
    for name, group in groups.items():
        n_ok = 0
        for net, x in group:
            ok = False
            for dx in (0.0, -0.85, 0.85, -1.3, 1.3, -1.7, 1.7):
                if not hits(f_rects, x + dx, y) and not hits(b_rects, x + dx, y):
                    ok = True
                    break
            n_ok += ok
        if n_ok == 16:
            print(f"  {name} all clear at y={y:.2f}")
    y += 0.4
print("\nfixed columns")
for x in (31.2, 32.0, 32.8, 33.6, 54.8, 56.2, 66.2, 68.4, 102.2, 103.5, 104.5):
    row = []
    y = 15.6
    while y <= 29.2:
        row.append("." if not hits(f_rects, x, y) and not hits(b_rects, x, y) else "X")
        y += 0.4
    print(f"x={x:5.1f} {''.join(row)}")
