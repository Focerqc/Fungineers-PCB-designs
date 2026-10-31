import re
from collections import Counter

p = r"qfbms32 ai pcb/qfbms32.kicad_pcb"
text = open(p, encoding="utf-8").read()
pat = re.compile(
    r"\(segment\s+"
    r"\(start ([0-9.]+) ([0-9.]+)\)\s+"
    r"\(end ([0-9.]+) ([0-9.]+)\)\s+"
    r"\(width ([0-9.]+)\)\s+"
    r"\(layer \"([^\"]+)\"\)\s+"
    r"\(net \"([^\"]+)\"\)"
)
segs = pat.findall(text)
print("segments", len(segs))
print("by layer", Counter(s[5] for s in segs))
print("by net")
for net, n in Counter(s[6] for s in segs).most_common():
    print(f"  {n:3d}  {net}")
print("via tokens", text.count("(via"))
print("zone tokens", text.count("(zone"))
print("C_F refs", len(re.findall(r"\(property \"Reference\" \"C_F", text)))
