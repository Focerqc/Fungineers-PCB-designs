"""Compare footprint positions between HEAD and the working PCB."""
import re
import subprocess
from pathlib import Path

cur = Path(r"qfbms32 ai pcb/qfbms32.kicad_pcb").read_text(encoding="utf-8")
old = subprocess.check_output(
    ["git", "show", "HEAD:qfbms32 ai pcb/qfbms32.kicad_pcb"],
    text=True,
    encoding="utf-8",
    errors="replace",
)


def fps(text):
    out = {}
    parts = re.split(r"\n\t\(footprint ", text)
    for p in parts[1:]:
        rm = re.search(r'\(property "Reference" "([^"]+)"', p)
        am = re.search(
            r"\n\t\t\(at ([0-9.\-]+) ([0-9.\-]+)(?: ([0-9.\-]+))?\)", p
        )
        if rm and am:
            out[rm.group(1)] = (
                float(am.group(1)),
                float(am.group(2)),
                float(am.group(3) or 0),
            )
    return out


A, B = fps(old), fps(cur)
print("old", len(A), "new", len(B))
moved = []
for r in sorted(set(A) | set(B)):
    if r not in A:
        moved.append((999, r, None, B[r], "ADDED"))
        continue
    if r not in B:
        moved.append((999, r, A[r], None, "REMOVED"))
        continue
    dx = B[r][0] - A[r][0]
    dy = B[r][1] - A[r][1]
    dr = B[r][2] - A[r][2]
    d = (dx * dx + dy * dy) ** 0.5
    if d > 0.05 or abs(dr) > 0.1:
        moved.append(
            (d, r, A[r], B[r], f"dx={dx:.2f} dy={dy:.2f} drot={dr:.1f}")
        )
moved.sort(reverse=True)
print("moved", len(moved))
for d, r, a, b, msg in moved:
    print(f"{d:7.2f} {r:12} {msg}")
    if a and b:
        print(f"         was {a} now {b}")
