import json
d = json.load(open(r"c:\Users\quinn\Documents\GitHub\Fungineers PCB designs\qfbms32 ai pcb\scratch\filter_geom.json", encoding="utf-8"))
F = []
for o in d["obstacles"]:
    if o["layer"].endswith("002003") or o["layer"].endswith("002000") or o["layer"].endswith("55555f"):
        F.append(o["bb"])
for s in d["segs"]:
    w = s["w"] / 2
    x1, x2 = sorted((s["x1"], s["x2"]))
    y1, y2 = sorted((s["y1"], s["y2"]))
    F.append((x1 - w, y1 - w, x2 + w, y2 + w))

def hit(x, y, keep):
    for a, b, c, d in F:
        dx = 0 if a <= x <= c else (a - x if x < a else x - c)
        dy = 0 if b <= y <= d else (b - y if y < b else y - d)
        if dx * dx + dy * dy < keep * keep:
            return True
    return False

def col_ok(x, y0, y1, keep=0.23):
    y = y0
    while y <= y1:
        if hit(x, y, keep):
            return False
        y += 0.25
    return True

for k in range(1, 33):
    p = [q for q in d["parts"][f"R_F{k}"]["pads"] if q["num"] == "2"][0]
    x = p["x"]
    best = None
    for dx in (0, 0.45, -0.45, 0.8, -0.8, 1.15, -1.15):
        if col_ok(x + dx, 16.7, 19.6) and not hit(x + dx, 16.7, 0.45) and not hit(x + dx, 19.6, 0.45):
            best = dx
            break
    print(f"{p['net']:10} x={x:.2f} lowband {best}")
