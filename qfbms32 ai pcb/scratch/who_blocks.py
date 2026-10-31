import json
d = json.load(open(r"c:\Users\quinn\Documents\GitHub\Fungineers PCB designs\qfbms32 ai pcb\scratch\filter_geom.json", encoding="utf-8"))
for o in d["obstacles"]:
    x1, y1, x2, y2 = o["bb"]
    if y2 < 19 or y1 > 26:
        continue
    if x2 < 36 or x1 > 104:
        continue
    if o["net"]:
        continue
    print(f"{o['ref']:8} p{o['num']:4} {o['layer'][-6:]} x {x1:.2f}-{x2:.2f} y {y1:.2f}-{y2:.2f}")
