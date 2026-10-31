"""Find clear lanes for the cell-filter fanout. Read-only."""
import json
from collections import defaultdict

p = r"c:\Users\quinn\Documents\GitHub\Fungineers PCB designs\qfbms32 ai pcb\scratch\filter_geom.json"
d = json.load(open(p, encoding="utf-8"))

print("--- all C_F ---")
for i in range(1, 33):
    cf = d["parts"][f"C_F{i}"]
    bits = []
    for pad in cf["pads"]:
        bb = [round(v, 3) for v in pad["bb"]]
        bits.append(f"p{pad['num']} {pad['net']} ({pad['x']:.3f},{pad['y']:.3f}) bb={bb}")
    print(f"C_F{i}", " || ".join(bits))

print("\n--- R_B pads ---")
for i in (1, 2, 17, 33):
    rb = d["parts"][f"R_B{i}"]
    print(i, "at", rb["x"], rb["y"], "rot", rb["rot"])
    for pad in rb["pads"]:
        print(" ", pad["num"], pad["net"], [round(v, 3) for v in pad["bb"]], "attr", pad["attr"])

print("\n--- footprints touching x=34..102 y=8..31, not R_F/C_F/R_B ---")
seen = set()
for o in d["obstacles"]:
    x, y = o["x"], o["y"]
    if not (34 <= x <= 102 and 8 <= y <= 31):
        continue
    ref = o["ref"]
    if ref.startswith(("R_F", "C_F", "R_B")):
        continue
    if ref in seen:
        continue
    seen.add(ref)
    part = d["parts"].get(ref)
    if part:
        print(f"{ref:10} {part['value'][:24]:24} ({part['x']:.2f},{part['y']:.2f}) rot={part['rot']} layer={part['layer']} pads={len(part['pads'])} attr0={part['pads'][0]['attr']} drill={part['pads'][0]['drill']}")
    else:
        print(ref, "no part entry", o["x"], o["y"])

print("\n--- J_CELL1 pads ---")
jc = d["parts"]["J_CELL1"]
for pad in jc["pads"]:
    print(pad["num"], pad["net"], "attr", pad["attr"], "drill", pad["drill"], [round(v, 3) for v in pad["bb"]])

print("\n--- F.Cu track X histogram near y 20-31 ---")
xs = defaultdict(int)
for s in d["segs"]:
    if s["layer"] != "F.Cu":
        continue
    # vertical?
    if abs(s["x1"] - s["x2"]) < 0.05:
        xs[round(s["x1"], 2)] += 1
print("vertical track x count", len(xs))
# print a few CELL tracks fully
print("sample segs", d["segs"][:4])
print("last segs", d["segs"][-3:])
