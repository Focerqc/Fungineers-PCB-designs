import pcbnew
from collections import defaultdict

PCB = r"c:\Users\quinn\Documents\GitHub\Fungineers PCB designs\qfbms32 ai pcb\qfbms32.kicad_pcb"
board = pcbnew.LoadBoard(PCB)

print("=== refs with no signal net ===")
for fp in sorted(board.GetFootprints(), key=lambda f: f.GetReference()):
    nets = sorted({p.GetNetname() for p in fp.Pads() if p.GetNetname()})
    if not nets:
        print(f"  {fp.GetReference():8} {fp.GetValue()}")

print("\n=== interesting refs ===")
for ref in ("BZ1", "J_USB1", "Q2", "R_CHG1", "R_CHG2", "D_CHG1", "D_CHG2", "U4", "U7"):
    fp = board.FindFootprintByReference(ref)
    if not fp:
        print(ref, "MISSING")
        continue
    pads = [f"{p.GetNumber()}={p.GetNetname() or '-'}" for p in fp.Pads() if p.GetNumber() not in ("",)]
    # unique numbered
    seen = []
    for p in fp.Pads():
        key = f"{p.GetNumber()}={p.GetNetname() or '-'}"
        if key not in seen and p.GetNumber():
            seen.append(key)
    print(f"{ref} {fp.GetValue()}: {', '.join(seen[:20])}")
