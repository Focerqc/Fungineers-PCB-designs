"""Which Y are clear on F.Cu for horizontal fanout lanes."""
import json

p = r"c:\Users\quinn\Documents\GitHub\Fungineers PCB designs\qfbms32 ai pcb\scratch\filter_geom.json"
d = json.load(open(p, encoding="utf-8"))

# F.Cu copper rectangles: SMD pads whose layer mask includes F.Cu, plus F.Cu tracks
# layer hex ...00002003 is F.Cu+mask+paste typically. B.Cu caps use a different mask.
# From dump, R_F layer ended 00002003. C_F didn't print layer in the second script.
# Collect pad bbs. Attr 1 = SMD. We'll classify by the layer field.

F_MASK = 0x2  # KiCad F.Cu is bit? In the hex L00000000_00000000_00000000_00002003
# KiCad layer set: F.Cu is layer 0, bit 0 of the copper layers... The FmtHex of LSET.
# 0x2003 = bits. Let's just print unique layer strings for a few refs.

layers = {}
for o in d["obstacles"]:
    layers.setdefault(o["layer"], []).append(o["ref"])
print("LAYER COUNTS")
for k, v in layers.items():
    print(k, len(v), "e.g.", v[0])
