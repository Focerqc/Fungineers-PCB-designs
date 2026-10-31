"""See if each source column can cross the lanes that actually pass through it."""
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
f_rects = []
b_rects = []
for o in d["obstacles"]:
    if o["layer"] in F_LAYERS:
        f_rects.append(o["bb"])
    elif o["layer"].endswith("0000800c") or o["layer"].endswith("00000004"):
        b_rects.append(o["bb"])
for s in d["segs"]:
    w = s["w"] / 2
    x1, x2 = sorted((s["x1"], s["x2"]))
    y1, y2 = sorted((s["y1"], s["y2"]))
    f_rects.append((x1 - w, y1 - w, x2 + w, y2 + w))

def dist_rect(x, y, box):
    x1, y1, x2, y2 = box
    dx = 0.0 if x1 <= x <= x2 else (x1 - x if x < x1 else x - x2)
    dy = 0.0 if y1 <= y <= y2 else (y1 - y if y < y1 else y - y2)
    return (dx * dx + dy * dy) ** 0.5

def track_clear(x, y0, y1, keep=0.25):
    for box in f_rects:
        # sample the segment
        y = min(y0, y1)
        hit = False
        while y <= max(y0, y1) + 1e-9:
            if dist_rect(x, y, box) < keep:
                hit = True
                break
            y += 0.2
        if hit:
            return False
    return True

def via_clear(x, y, keep=0.45):
    for box in f_rects + b_rects:
        if dist_rect(x, y, box) < keep:
            return False
    return True

# southmost cap pad per monitor net
caps = {}
for i in range(1, 33):
    cf = d["parts"][f"C_F{i}"]
    for p in cf["pads"]:
        caps.setdefault(p["net"], []).append((p["x"], p["y"]))

nets = []
for k in range(1, 33):
    p2 = [p for p in d["parts"][f"R_F{k}"]["pads"] if p["num"] == "2"][0]
    pts = caps[p2["net"]]
    south = max(pts, key=lambda q: q[1])
    nets.append({"net": p2["net"], "sx": p2["x"], "tx": south[0], "ty": south[1]})

for group in (nets[:16], nets[16:]):
    print("---", group[0]["net"], "to", group[-1]["net"])
    # lane y high to low, index 0 is nearest the resistors
    pitch = 0.40
    base = 22.6
    for i, n in enumerate(group):
        n["lane"] = base - i * pitch
    taken = []
    ok_n = 0
    for i, n in enumerate(group):
        ys = []
        for j, m in enumerate(group):
            if j == i:
                continue
            if m["lane"] <= n["lane"]:
                continue
            lo, hi = sorted((m["sx"], m["tx"]))
            if lo - 0.2 < n["sx"] < hi + 0.2:
                ys.append(m["lane"])
        # drop from this lane down to 15.7 at tx also crosses lower horizontals that cover tx
        drop_ys = []
        for j, m in enumerate(group):
            if m["lane"] >= n["lane"]:
                continue
            lo, hi = sorted((m["sx"], m["tx"]))
            if lo - 0.2 < n["tx"] < hi + 0.2:
                drop_ys.append(m["lane"])
        src_dx = 0.0
        if ys:
            y_hi, y_lo = max(ys) + 0.35, min(ys) - 0.35
            src_dx = None
            offsets = [0.0]
            for k in range(1, 8):
                offsets.extend((k * 0.15, -k * 0.15))
            for dx in offsets:
                x = n["sx"] + dx
                if any(abs(x - t) < 0.55 for t in taken):
                    continue
                if any(abs(x - m["sx"]) < 0.55 and m is not n for m in group):
                    continue
                if track_clear(x, y_lo, y_hi) and via_clear(x, y_lo) and via_clear(x, y_hi):
                    src_dx = dx
                    break
        drop_dx = 0.0
        if drop_ys:
            y_hi, y_lo = max(drop_ys) + 0.35, 15.55
            drop_dx = None
            offsets = [0.0]
            for k in range(1, 10):
                offsets.extend((k * 0.15, -k * 0.15))
            for dx in offsets:
                x = n["tx"] + dx
                if track_clear(x, y_lo, y_hi) and via_clear(x, y_hi) and via_clear(x, y_lo):
                    drop_dx = dx
                    break
        good = src_dx is not None and drop_dx is not None
        if good:
            ok_n += 1
            taken.append(n["sx"] + src_dx)
        print(
            f"  {'OK' if good else 'NO'} {n['net']:10} src_cross {len(ys):2d} dx={src_dx} "
            f"drop_cross {len(drop_ys):2d} ddx={drop_dx} lane {n['lane']:.2f}"
        )
    print("  fit", ok_n, "/", len(group))
