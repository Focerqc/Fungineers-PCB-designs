import json
from collections import Counter
from pathlib import Path

d = json.loads(Path("qfbms32 ai pcb/qfbms32_erc.json").read_text(encoding="utf-8"))
types = Counter()
samples = {}
for s in d["sheets"]:
    for v in s.get("violations", []):
        t = v.get("type", "?")
        types[t] += 1
        if t not in samples:
            samples[t] = []
        if len(samples[t]) < 5:
            items = v.get("items", [])
            desc = v.get("description", v.get("message", ""))
            pos = []
            for it in items:
                pos.append(
                    {
                        "desc": it.get("description", "")[:80],
                        "pos": it.get("pos"),
                    }
                )
            samples[t].append({"desc": desc, "items": pos})

print("TYPES", dict(types))
for t, ss in samples.items():
    print("\n===", t, "===")
    for s in ss:
        print(s["desc"])
        for it in s["items"]:
            print(" ", it)
