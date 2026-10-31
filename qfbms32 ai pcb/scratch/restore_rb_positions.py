"""Restore R_B1..R_B33 to the positions committed on HEAD.

A routing script parked them on the top edge (y=1.8). The committed
placement is the pixel-matched row at y≈28.05 next to the cell connectors.
"""
from __future__ import annotations

import re
import shutil
import subprocess
from pathlib import Path

import pcbnew

ROOT = Path(__file__).resolve().parents[1]
PCB = ROOT / "qfbms32.kicad_pcb"
HIST = ROOT / ".history"


def committed_rb() -> dict[str, tuple[float, float, float]]:
    text = subprocess.check_output(
        ["git", "show", "HEAD:qfbms32 ai pcb/qfbms32.kicad_pcb"],
        cwd=ROOT.parent,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    out = {}
    for p in re.split(r"\n\t\(footprint ", text)[1:]:
        rm = re.search(r'\(property "Reference" "(R_B\d+)"', p)
        am = re.search(r"\n\t\t\(at ([0-9.\-]+) ([0-9.\-]+)(?: ([0-9.\-]+))?\)", p)
        if rm and am:
            out[rm.group(1)] = (
                float(am.group(1)),
                float(am.group(2)),
                float(am.group(3) or 0),
            )
    return out


def main() -> None:
    want = committed_rb()
    if len(want) < 33:
        raise SystemExit(f"expected 33 R_B in HEAD, found {len(want)}")
    HIST.mkdir(exist_ok=True)
    shutil.copy2(PCB, HIST / "qfbms32_pre_restore_rb.kicad_pcb")
    board = pcbnew.LoadBoard(str(PCB))
    for ref, (x, y, rot) in sorted(want.items(), key=lambda kv: int(kv[0][3:])):
        fp = board.FindFootprintByReference(ref)
        if not fp:
            print("missing", ref)
            continue
        fp.SetPosition(pcbnew.VECTOR2I(pcbnew.FromMM(x), pcbnew.FromMM(y)))
        fp.SetOrientation(pcbnew.EDA_ANGLE(rot, pcbnew.DEGREES_T))
        p = fp.GetPosition()
        print(f"{ref} -> {pcbnew.ToMM(p.x):.3f}, {pcbnew.ToMM(p.y):.3f} rot {rot:g}")
    pcbnew.SaveBoard(str(PCB), board)
    print("saved", PCB)


if __name__ == "__main__":
    main()
