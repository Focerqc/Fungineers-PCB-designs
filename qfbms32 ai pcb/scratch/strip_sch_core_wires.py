"""
Remove stub wires+labels in the crowded core schematic region (BQ/SSR/FET)
that were falsely shorting pins. Keep R_F/C_F/connector/power discrete
wiring in the empty banks (y>=280 or x>=440).
Also keep pre-existing ESP/CAN labels.
"""
from __future__ import annotations

import re
from pathlib import Path

SCH = Path(__file__).resolve().parents[1] / "qfbms32.kicad_sch"


def main():
    sch = SCH.read_text(encoding="utf-8")

    # Remove wire+following label pairs where wire start is in core region
    def drop_pair(m: re.Match) -> str:
        x0, y0 = float(m.group(1)), float(m.group(2))
        # keep empty banks
        if y0 >= 280 or x0 >= 440:
            return m.group(0)
        return ""

    sch2 = re.sub(
        r"\n\t\(wire\n"
        r"\t\t\(pts\n"
        r"\t\t\t\(xy ([0-9.-]+) ([0-9.-]+)\) \(xy [0-9.-]+ [0-9.-]+\)\n"
        r"\t\t\)\n"
        r"\t\t\(stroke \(width 0\) \(type default\)\)\n"
        r'\t\t\(uuid "[^"]+"\)\n'
        r"\t\)\n"
        r'\t\(label "[^"]+"\n'
        r"\t\t\(at [^\n]+\n"
        r"\t\t\(effects [^\n]+\n"
        r'\t\t\(uuid "[^"]+"\)\n'
        r"\t\)",
        drop_pair,
        sch,
    )
    # Also one-line pts variant if any
    sch2 = re.sub(
        r"\n\t\(wire\n"
        r"\t\t\(pts \(xy ([0-9.-]+) ([0-9.-]+)\) \(xy [0-9.-]+ [0-9.-]+\)\)\n"
        r"\t\t\(stroke \(width 0\) \(type default\)\)\n"
        r'\t\t\(uuid "[^"]+"\)\n'
        r"\t\)\n"
        r'\t\(label "[^"]+"\n'
        r"\t\t\(at [^\n]+\n"
        r"\t\t\(effects [^\n]+\n"
        r'\t\t\(uuid "[^"]+"\)\n'
        r"\t\)",
        drop_pair,
        sch2,
    )

    SCH.write_text(sch2, encoding="utf-8")
    print("stripped core wires; wires left", sch2.count("(wire"))
    print("labels left", len(re.findall(r"\(label ", sch2)))


if __name__ == "__main__":
    main()
