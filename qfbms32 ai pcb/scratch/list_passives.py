import pcbnew
from collections import Counter

b = pcbnew.LoadBoard(r"qfbms32 ai pcb/qfbms32.kicad_pcb")
rows = []
for fp in b.GetFootprints():
    r = fp.GetReference()
    if r.startswith(("R_F", "R_B", "C_")):
        rows.append((r, fp.GetValue(), str(fp.GetFPID().GetLibItemName())))
for r, v, fp in sorted(rows):
    print(f"{r:8} {v:12} {fp}")
print("--- value counts R_F ---")
print(Counter(v for r, v, _ in rows if r.startswith("R_F")))
print("--- value counts R_B ---")
print(Counter(v for r, v, _ in rows if r.startswith("R_B")))
print("--- caps ---")
print(Counter((r, v) for r, v, _ in rows if r.startswith("C_")))

# BQ pin names sample
for ref in ("U_BQ1", "U_BQ2"):
    fp = b.FindFootprintByReference(ref)
    print(f"=== {ref} pads with names ===")
    for pad in sorted(fp.Pads(), key=lambda p: p.GetNumber()):
        n = pad.GetNumber()
        # only show first few / named interest
        if n in [str(i) for i in range(1, 49)] + ["49", "EP"]:
            pass
    # print pin name from pad netname empty; footprint may not have pin names
    print(" pad count", fp.GetPadCount())
